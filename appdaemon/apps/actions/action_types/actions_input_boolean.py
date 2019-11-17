#
# this is a basic input_boolean action.
# input_boolean can only have value on or off.
# action example:
# input_boolean.anything: {"value": "on"}
# or
# input_boolean.anything:
#   value: "on"
#


import appdaemon.plugins.hass.hassapi as hass

class actions_input_boolean(hass.Hass):

    def initialize(self):
        return

    def action(self, kwargs):
        entity = kwargs["entity"]
        entity_settings = kwargs["entity_settings"]
        self.call_service("homeassistant/turn_" + entity_settings["value"], entity_id = entity)
