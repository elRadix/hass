#
# this is a basic light action.
# light can only have value on or off and settings brightness and rgb_color.
# action example:
# light.anything: {"value": "on", "brightness: 125","rgb_color": [255, 127, 0]}
# or
# switch.anything:
#   value: "on"
#   brightness: 125
#   rgb_color:
#     - 255
#     - 127
#     - 0
#

import appdaemon.plugins.hass.hassapi as hass

class actions_light(hass.Hass):

    def initialize(self):
        return

    def action(self, kwargs):
        entity = kwargs["entity"]
        entity_settings = kwargs["entity_settings"]
        #self.log(entity_settings)
        if entity_settings["value"] == "on":
            if "brightness" in entity_settings and "rgb_color" in entity_settings:
                self.turn_on(entity, rgb_color = entity_settings["rgb_color"], brightness = entity_settings["brightness"])
            elif "brightness" in entity_settings:
                self.turn_on(entity, brightness = entity_settings["brightness"])
            elif "rgb_color" in entity_settings:
                self.turn_on(entity, rgb_color = entity_settings["rgb_color"])
            else:
                self.turn_on(entity)
        elif entity_settings["value"] == "off":
            self.turn_off(entity)
        elif "preset" in entity_settings["value"]:
            type = entity_settings["value"][7:]
            light_settings_app = self.get_app("light_settings")
            color, brightness, effect_white = light_settings_app.lightsettings(entity, type)
            if effect_white and brightness != None:
                self.turn_on(entity, effect = "white")
                self.turn_on(entity, brightness = brightness)
                return
            elif effect_white:
                self.turn_on(entity, effect = "white")
                return
            if color != None and brightness != None:
                self.turn_on(entity, rgb_color = color, brightness = brightness)
            elif brightness != None:
                self.turn_on(entity, brightness = brightness)
            elif color != None:
                self.turn_on(entity, rgb_color = color)
            else:
                self.turn_on(entity)
        else:
            self.log("Wrong setting for light {}".format(entity))
