#
# this is a basic switch action.
# switch can only have value on or off.
# action example:
# switch.anything: {"value": "on"}
# or
# switch.anything:
#   value: "on"
#

import appdaemon.plugins.hass.hassapi as hass

class actions_switch(hass.Hass):

    def initialize(self):
        return

    def action(self, kwargs):
        entity = kwargs["entity"]
        entity_settings = kwargs["entity_settings"]
        self.call_service("homeassistant/turn_" + entity_settings["value"], entity_id = entity)
