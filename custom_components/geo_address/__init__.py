from geopy.geocoders import Nominatim
from datetime import datetime, timedelta, timezone
import json
import logging
import time
import urllib.request
import voluptuous as vol

import homeassistant
from homeassistant.components import device_tracker
from homeassistant.const import (ATTR_ENTITY_ID, SERVICE_TURN_OFF,
                                 SERVICE_TURN_ON, STATE_OFF, STATE_ON,
                                 CONF_ENTITIES, CONF_EXCLUDE, CONF_INCLUDE)
from homeassistant.core import State
import homeassistant.helpers.config_validation as cv
import homeassistant.helpers.discovery
from homeassistant.helpers.event import async_call_later, async_track_time_interval, async_track_state_change
from typing import Any

DEPENDENCIES = ['device_tracker']

DOMAIN = 'geo_address'
ENTITY_ID_FORMAT = DOMAIN + '.{}'

CONF_USE_STATE              = "use_state"
CONF_USE_TIMER              = "use_timed"
CONF_INTERVAL               = 'update_interval'
CONF_PERIOD                 = 'update_period'
CONF_FIELDS_DISPLAY         = 'fields_display'
CONF_EXCLUDED_IDS           = 'excluded_ids'
CONF_FIELDS_DISPLAY_DEFAULT = "road village city county state postcode country"

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_USE_STATE): cv.boolean,
        vol.Optional(CONF_USE_TIMER): cv.boolean,
        vol.Optional(CONF_INTERVAL): cv.string,
        vol.Optional(CONF_PERIOD): cv.string,
        vol.Optional(CONF_EXCLUDED_IDS): cv.string,
        vol.Optional(CONF_EXCLUDE, default={}): vol.Schema({
            vol.Optional(CONF_ENTITIES, default=[]): cv.entity_ids,
        }),
        vol.Optional(CONF_INCLUDE, default={}): vol.Schema({
            vol.Optional(CONF_ENTITIES, default=[]): cv.entity_ids,
        }),
        vol.Optional(CONF_FIELDS_DISPLAY): cv.match_all
    })
}, extra=vol.ALLOW_EXTRA)

_LOGGER     = logging.getLogger('custom_components.geo_address')

async def async_setup(hass, config):
    geoaddress = GeoAddress(hass, config[DOMAIN])

    # Make sure there are states for all location_devices
    async_call_later(hass, 1, geoaddress.create_defaults)

    # Use timed updates
    if CONF_USE_TIMER in config[DOMAIN] and config[DOMAIN].get(CONF_USE_TIMER) == True:
        _LOGGER.debug('- Using timed updates')
        async_track_time_interval(hass, geoaddress.update_address_time, timedelta(seconds=int(config[DOMAIN].get(CONF_INTERVAL))))

    # Use state update
    if CONF_USE_STATE in config[DOMAIN] and config[DOMAIN].get(CONF_USE_STATE) == True:
        _LOGGER.debug('- Using state updates')
        for tracker_id in geoaddress.ids:
            async_track_state_change(hass, tracker_id, geoaddress.update_address_state,
                                     from_state=None, to_state=None)
            _LOGGER.debug('Added tracker for ' + tracker_id)

    return True

class GeoAddress:
    """GeoAddress controller."""

    def __init__(self, hass, config):
        """Initialize."""
        _LOGGER.debug('############################################')
        _LOGGER.debug('#                                          #')
        _LOGGER.info(' # GeoAddress starting to track geo changes #')
        _LOGGER.debug('#                                          #')
        _LOGGER.debug('############################################')

        self._hass   = hass
        self._config = config
        self._ids = []

        # Make a list of the tracker ids to follow
        include = config.get(CONF_INCLUDE, {})
        exclude = config.get(CONF_EXCLUDE, {})
        whitelist = set(include.get(CONF_ENTITIES, []))
        blacklist = set(exclude.get(CONF_ENTITIES, []))

        # If whitelist is configured, use it, else get all device_trackers
        trackers = whitelist if whitelist else self._hass.states.async_entity_ids("device_tracker")

        for tracker in trackers:
            if not blacklist or tracker not in blacklist:
                self._ids.append(tracker)

    @property
    def config(self):
        """ Return the config """
        return self._config

    @config.setter
    def config(self, config):
        self._config = config

    @property
    def hass(self):
        """ Return the hass instance """
        return self._hass

    @hass.setter
    def ids(self, hass):
        self._hass = hass

    @property
    def ids(self):
        """ Return the list of prepared device_tracker ids """
        return self._ids

    @ids.setter
    def ids(self, ids):
        self._ids = ids

    def create_defaults(self, time):
        """ Create default entities """
        for tracker_id in self.ids:
            entity_id = ENTITY_ID_FORMAT.format(tracker_id.split('.', 1)[1])
            state_obj = self.hass.states.get(entity_id)
            if state_obj is None:
                self.update_address(tracker_id)

    def update_address_time(self, now=None):
        for tracker_id in self.ids:
            self.update_address(tracker_id)

    def update_address_state(self, entity_id, old_state, new_state):
        self.update_address(entity_id)

    def update_address(self, entity_id):
        _LOGGER.debug("Updating address for " + entity_id)

        try:
            state = self.hass.states.get(entity_id)
            last_updated = state.last_updated
            now = datetime.now(timezone.utc) - timedelta(seconds=int(self.config.get(CONF_PERIOD)))

            # Only update entities where an update has occurred within the REVERSE time
            #  also double check the entity has a position
            if "latitude" in state.attributes and last_updated > now:
                geolocator = Nominatim(user_agent=DOMAIN)
                location = geolocator.reverse(str(state.attributes["latitude"]) + "," + str(state.attributes["longitude"]))
                address = location.raw["address"]

                fields = self.config.get(CONF_FIELDS_DISPLAY, CONF_FIELDS_DISPLAY_DEFAULT).split(" ")

                # Check city / county duplicate values
                if ('city' in fields and 'county' in fields) and (address.get('city') == address.get('county')):
                    fields.remove('county')

                output = ""
                for field in fields:
                    output += address.get(field, "") + " "

                # entity_id is device_tracker.name_name to start with
                entity_id = ENTITY_ID_FORMAT.format(entity_id.split('.', 1)[1])

                # Set the state
                self.hass.states.set(entity_id, output, address)

                _LOGGER.debug("Saved new value for " + entity_id)

        except Exception as e:
            _LOGGER.error("Failed to lookup address :: " + str(e))