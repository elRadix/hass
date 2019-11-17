#
# this is a fade action for lights.
# action example:
# fade_in: {"value": "light.anything","step": 15, "pause": 0.5,"max": 255}

import appdaemon.plugins.hass.hassapi as hass
import time

class actions_fade_in_light(hass.Hass):

    def initialize(self):
        return

    def action(self, kwargs):
        entity_settings = kwargs["entity_settings"]
        light = entity_settings["value"]
        max = 255
        delay = 0.5
        step = 15
        start = 0
        if "max" in entity_settings:
            max = entity_settings["max"]
        if "pause" in entity_settings:
            delay = entity_settings["pause"]
        if "step" in entity_settings:
            step = entity_settings["step"]
        if "start" in entity_settings:
            brightness = entity_settings["start"]
        else:      
            brightness = self.get_state(light, attribute="brightness")
        if brightness == None:
            brightness = 0
        else:
            brightness = int(brightness)
        brightness = brightness + step
        while brightness < max:
            self.turn_on(light, brightness = brightness)
            time.sleep(delay)
            brightness = brightness + step
