#
# this is a basic input_number action.
# input_number can only have numeric value.
# action example:
# input_number.anything: {"value": 56}
# or
# input_number.anything:
#   value: 56
#

import appdaemon.plugins.hass.hassapi as hass

class actions_input_number(hass.Hass):

    def initialize(self):
        return

    def action(self, kwargs):
        entity = kwargs["entity"]
        entity_settings = kwargs["entity_settings"]
        self.call_service("input_number/set_value", entity_id = entity, value = entity_settings["value"])
