#
# this is a fade action for lights.
# action example:
# fade_out: {"value": "light.anything","step": 15, "pause": 0.5,"max": 255}

import appdaemon.plugins.hass.hassapi as hass
import time

class actions_fade_out_light(hass.Hass):

    def initialize(self):
        return

    def action(self, kwargs):
        entity_settings = kwargs["entity_settings"]
        light = entity_settings["value"]
        delay = 0.5
        step = 15
        if "pause" in entity_settings:
            delay = entity_settings["pause"]
        if "step" in entity_settings:
            step = entity_settings["step"]
        brightness = self.get_state(light, attribute="brightness")
        if brightness == None:
            brightness = 0
        else:
            brightness = int(brightness)
        brightness = brightness - step
        while brightness > 0:
            self.turn_on(light, brightness = brightness)
            time.sleep(delay)
            brightness = brightness - step
        self.turn_off(light)