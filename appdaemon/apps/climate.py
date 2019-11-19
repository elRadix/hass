import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
class climate(hass.Hass):

 def initialize(self):
   self.listen_state(self.climate_cb, self.args)

 def climate_cb(self, entity, attribute, old, new, kwargs):
   friendly = self.get_state(entity, attribute="friendly_name")
   if old == "off" and new == "heat":
    if self.get_state('switch.easyplus') != 'on':
      self.turn_on('switch.easyplus')
      self.log("easyplus on")
    time.sleep(30)
    if self.get_state('input_boolean.easyplus_boiler_heating') != 'on':
      self.turn_on('input_boolean.easyplus_boiler_heating')
      self.log("boiler on")
    self.call_service("shell_command/heating_"+friendly)
    self.log("target temperature set")
    return
   if old == "heat" and new == "off":
    self.call_service("climate/set_temperature", entity_id = self.args["climate"], temperature = 5)
    self.call_service("shell_command/heating_tmp_"+friendly+"_off")
    self.log("target temperature off")
    return

