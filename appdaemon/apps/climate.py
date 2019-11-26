import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
class climate(hass.Hass):

 def initialize(self):
   self.listen_state(self.climate_cb, self.args["climate"])

 def climate_cb(self, entity, attribute, old, new, kwargs):
   friendly = self.get_state(entity, attribute="friendly_name")
   boiler = self.get_state('input_boolean.easyplus_boiler_heating')
   easyplus = self.get_state('binary_sensor.easyplus_telnet')
   current_temp= self.get_state(entity, attribute="current_temperature")
   heating_temp= self.get_state(entity, attribute="temperature")
   if old == "off" and new == "heat":
    if easyplus != 'on':
      for i in range (0, 5, 1):
        self.turn_off('switch.easyplus')
        self.turn_on('switch.easyplus')
        tg = "Easyplus is rebooting state is {} ".format(easyplus)
        self.call_service("notify/dageraad",message = tg)
        time.sleep(25)
        self.log("easyplus %s", easyplus)
        tg = "Easyplus ready, state is {} ".format(easyplus)
        self.call_service("notify/dageraad",message = tg)
    if boiler != 'on':
      self.turn_on('input_boolean.easyplus_boiler_heating')
      self.log("boiler %s", boiler)
      tg = "Boiler is {} ".format(easyplus)
      self.call_service("notify/dageraad",message = tg)
    self.call_service("shell_command/heating_"+friendly)
    self.set_state("sensor.notify_message", state="Heating started")
    self.log("target temperature set")
    self.call_service('notify/dageraad',
        title="[Heating Started]\n",
        message=("\n\nRoom {}\nCurrent temp is {}\nHeating temp set to {}".format(friendly,current_temp,heating_temp)))
    return
   if old == "heat" and new == "off":
    self.call_service("climate/set_temperature", entity_id = self.args["climate"], temperature = 5)
    self.call_service("shell_command/heating_tmp_"+friendly+"_off")
    self.log("target temperature off")
    heating_temp_off= self.get_state(entity, attribute="temperature")
    self.set_state("sensor.notify_message", state="Heating Completed")
    self.call_service('notify/dageraad',
        title="[Heating Completed]\n",
        message=("\nRoom {}\nCurrent temp is {}\nHeating temp set to {}".format(friendly,current_temp,heating_temp_off)))
    return
   self.log(self.args)

#  def temp_state(self, entity, attribute, old, new, kwargs):
#    self.temp_state = int(float(self.get_state(self.args["temp"])))
#    self.get_state(self.temp_ste, attribute="temperature") != self.kwargs["ACTempID"]:
#    friendly = self.get_state(entity, attribute="friendly_name")
#    tg = "Current temp for {} is {} ".format(friendly, temp_state)
#    self.call_service("notify/dageraad",message = tg)



#  def initialize(self):
#    self.listen_state(self.climate_cb, self.args["climate"])
#    self.listen_state(self.temp_state, self.args["temp"])

#  def climate_cb(self, entity, attribute, old, new, kwargs):
#    friendly = self.get_state(entity, attribute="friendly_name")
#    easyplus = self.get_state('binary_sensor.easyplus_telnet')
#    boiler = self.get_state('input_boolean.easyplus_boiler_heating')
#    tg = "Easyplus is {} ".format(easyplus)
#    self.call_service("notify/dageraad",message = tg)
#    self.log("telnet state is %s ", easyplus)
#    if old == "off" and new == "heat":
#     while self.get_state('binary_sensor.easyplus_telnet') == 'off':
#       self.turn_off('switch.easyplus')
#       self.turn_on('switch.easyplus')
#       time.sleep(50)
#       self.log("telnet state is %s", easyplus)
#       tg = "Easyplus is {} ".format(easyplus)
#       self.call_service("notify/dageraad",message = tg)
#     if self.get_state('input_boolean.easyplus_boiler_heating') != 'on':
#       self.turn_on('input_boolean.easyplus_boiler_heating')
#       self.log("Boiler is {} .".format(boiler))
#       tg = "Heating program starting for room: {} ".format(friendly)
#       tg2 = "Boiler is {} for room: {} ".format(boiler, friendly)
#       self.call_service("notify/dageraad",message = tg)
#       self.call_service("notify/dageraad",message = tg2)
#     self.call_service("shell_command/heating_"+friendly)
#     self.log("target temperature set")
#     return
#    if old == "heat" and new == "off":
#     self.call_service("climate/set_temperature", entity_id = self.args["climate"], temperature = 5)
#     self.call_service("shell_command/heating_tmp_"+friendly+"_off")
#     self.log("target temperature off")
#     tg = "Heating progam completed for room: {} ".format(friendly)
#     self.call_service("notify/dageraad",message = tg)
#     return
#    self.log(self.args)

#  def temp_state(self, entity, attribute, old, new, kwargs):
#    self.temp_state = int(float(self.get_state(self.args["temp"])))
#    friendly = self.get_state(entity, attribute="friendly_name")
#    tg = "Current temp for {} is {} ".format(friendly, temp_state)
#    self.call_service("notify/dageraad",message = tg)
