# import appdaemon.plugins.hass.hassapi as hass
# import datetime
# import time
# class climate(hass.Hass):

#  def initialize(self):
#    self.listen_state(self.climate_cb, self.args["climate"])

#  def climate_cb(self, entity, attribute, old, new, kwargs):
#    friendly = self.get_state(entity, attribute="friendly_name")
#    easyplus = self.get_state('sensor.easyplus_telnet')
#    if old == "off" and new == "heat":
#     while self.get_state('sensor.easyplus') == 'off':
#       self.turn_off('switch.easyplus')
#       self.turn_on('switch.easyplus')
#       time.sleep(40)
#       self.log("easyplus on")
#     if self.get_state('input_boolean.easyplus_boiler_heating_dev') != 'on':
#       self.turn_on('input_boolean.easyplus_boiler_heating_dev')
#       self.log("boiler on")
#     self.call_service("shell_command/heating_"+friendly)
#     self.log("target temperature set")
#     return
#    if old == "heat" and new == "off":
#     self.call_service("climate/set_temperature", entity_id = self.args["climate"], temperature = 5)
#     self.call_service("shell_command/heating_tmp_"+friendly+"_off")
#     self.log("target temperature off")
#     return
#    self.log(self.args)

import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
class climate(hass.Hass):

 def initialize(self):
   self.listen_state(self.climate_cb, self.args["climate"])

 def climate_cb(self, entity, attribute, old, new, kwargs):
   friendly = self.get_state(entity, attribute="friendly_name")
   if old == "off" and new == "heat":
    if self.get_state('switch.easyplus') != 'on':
      self.turn_on('switch.easyplus')
      time.sleep(20)
      self.log("easyplus on")
    if self.get_state('input_boolean.easyplus_boiler_heating_dev') != 'on':
      self.turn_on('input_boolean.easyplus_boiler_heating_dev')
      self.log("boiler on")
    self.call_service("shell_command/heating_"+friendly)
    self.log("target temperature set")
    return
   if old == "heat" and new == "off":
    self.call_service("climate/set_temperature", entity_id = self.args["climate"], temperature = 5)
    self.call_service("shell_command/heating_tmp_"+friendly+"_off")
    self.log("target temperature off")
    return
   self.log(self.args)