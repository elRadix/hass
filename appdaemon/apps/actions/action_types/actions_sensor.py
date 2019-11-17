#
# this is a basic sensor action.
# sensor can only have any value.
# action example:
# sensor.anything: {"value": "something"}
# or
# sensor.anything:
#   value: anything
#

import appdaemon.plugins.hass.hassapi as hass

class actions_sensor(hass.Hass):

    def initialize(self):
        return

    def action(self, kwargs):
        entity = kwargs["entity"]
        entity_settings = kwargs["entity_settings"]
        self.set_state(entity, state=entity_settings["value"])
