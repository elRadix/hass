import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
class climate(hass.Hass):

 def initialize(self):
   self.listen_state(self.climate_cb, self.args["climate"])
   self.listen_state(self.temp_state, self.args["temp"])

 def climate_cb(self, entity, attribute, old, new, kwargs):
   friendly = self.get_state(entity, attribute="friendly_name")
   easyplus = self.get_state('binary_sensor.easyplus_telnet')
   boiler = self.get_state('input_boolean.easyplus_boiler_heating')
  #  self.temp = int(float(self.get_state(self.args["friendly"])))
  #  friendly = self.get_state(climate, attribute="friendly_name")
  #  tg = "Current temp is {} for room: {} ".format(temp, friendly)
   self.call_service("notify/dageraad",message = tg)
   self.log("telnet state is %s ", easyplus)
   tg = "Easyplus is {} ".format(easyplus)
   self.call_service("notify/dageraad",message = tg)
   if old == "off" and new == "heat":
    while self.get_state('binary_sensor.easyplus_telnet') == 'off':
      self.turn_off('switch.easyplus')
      self.turn_on('switch.easyplus')
      time.sleep(50)
      self.log("telnet state is %s", easyplus)
      tg = "Easyplus is {} ".format(easyplus)
      self.call_service("notify/dageraad",message = tg)
    if self.get_state('input_boolean.easyplus_boiler_heating') != 'on':
      self.turn_on('input_boolean.easyplus_boiler_heating_dev')
      self.log("Boiler is {} .".format(boiler))
      tg = "Heating program starting for room: {} ".format(friendly)
      tg2 = "Boiler is {} for room: {} ".format(boiler, friendly)
      self.call_service("notify/dageraad",message = tg)
      self.call_service("notify/dageraad",message = tg2)
    self.call_service("shell_command/heating_"+friendly)
    self.log("target temperature set")
    return
   if old == "heat" and new == "off":
    self.call_service("climate/set_temperature", entity_id = self.args["climate"], temperature = 5)
    self.call_service("shell_command/heating_tmp_"+friendly+"_off")
    self.log("target temperature off")
    tg = "Heating progam completed for room: {} ".format(friendly)
    self.call_service("notify/dageraad",message = tg)
    return
   self.log(self.args)

 def temp_state(self, entity, attribute, old, new, kwargs):
   tg = "Current temp is {} ".format(temp_state)
   self.call_service("notify/dageraad",message = tg)

# import appdaemon.plugins.hass.hassapi as hass
# import datetime
# import time
# class climate(hass.Hass):

#  def initialize(self):
#    self.listen_state(self.climate_cb, self.args["climate"])

#  def climate_cb(self, entity, attribute, old, new, kwargs):
#    friendly = self.get_state(entity, attribute="friendly_name")
#    if old == "off" and new == "heat":
#     if self.get_state('switch.easyplus') != 'on':
#       self.turn_on('switch.easyplus')
#       time.sleep(20)
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