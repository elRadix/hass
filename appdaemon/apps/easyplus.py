import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
class easyplus(hass.Hass):

 def initialize(self):
   self.listen_state(self.easyplus_cb, self.args["entity"])

 def easyplus_cb(self, entity, attribute, old, new, kwargs):
   friendly = self.get_state(entity, attribute="friendly_name")
   state = self.get_state(entity)
   easyplus = self.get_state('binary_sensor.easyplus_telnet')
   self.log("%s %s", friendly, state)
   if old != "on" and new != "off":
    if easyplus != 'on':
      for i in range (3):
        self.turn_off('switch.easyplus')
        self.turn_on('switch.easyplus')
        time.sleep(10)
        self.log("easyplus %s", easyplus)
        self.turn_off(entity)
        self.turn_on(entity)
        self.log("%s %s", friendly, state)
    return
#   self.log(self.args)
