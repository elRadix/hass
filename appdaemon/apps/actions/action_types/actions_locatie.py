#
# this is actually a basic sensor action.
# but because i got a special sensor that stores location from active persons in the home app i can use this
# sensor can only have any value.
# you could change this to create your own notify action
# action example:
# locatie: {"value": "some location"}
# or
# locatie:
#   value: some location
#

import appdaemon.plugins.hass.hassapi as hass

class actions_locatie(hass.Hass):

    def initialize(self):
        return

    def action(self, kwargs):
        entity = kwargs["entity"]
        entity_settings = kwargs["entity_settings"]
        entity = "sensor.locatie_" + self.get_state("sensor.actieve_persoon").lower()
        self.set_state(entity, state=entity_settings["value"])
