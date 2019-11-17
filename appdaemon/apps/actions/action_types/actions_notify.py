#
# this is actually a basic sensor action.
# but because i got a special sensor that triggers my notify app i can use this
# sensor can only have any value.
# you could change this to create your own notify action
# action example:
# notify: {"value": "any kind of message"}
# or
# notify:
#   value: any kind of message
#

import appdaemon.plugins.hass.hassapi as hass

class actions_notify(hass.Hass):

    def initialize(self):
        return

    def action(self, kwargs):
        entity = kwargs["entity"]
        entity_settings = kwargs["entity_settings"]
        self.set_state("sensor.notify_message", state=entity_settings["value"])
