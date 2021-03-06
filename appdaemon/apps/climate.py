import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
class climate(hass.Hass):

 def initialize(self):
   self.listen_state(self.climate_cb, self.args["climate"])

 def climate_cb(self, entity, attribute, old, new, kwargs):
   friendly = self.get_state(entity, attribute="friendly_name")
   boiler = self.get_state('input_boolean.easyplus_boiler_heating')
   telnet = self.get_state('binary_sensor.easyplus_telnet')
   easyplus = self.get_state('switch.easyplus')


   if old == "off" and new == "heat":
    while self.get_state('binary_sensor.easyplus_telnet') == 'off':
      self.turn_off('switch.easyplus')
      self.turn_on('switch.easyplus')
      time.sleep(20)
      self.get_state('switch.easyplus')
      self.log("telnet state is %s", telnet)
      tg = "Easyplus is {}, Telnet state is {} ".format(easyplus, telnet)
      self.call_service("notify/dageraad",message = tg)

    if boiler != 'on':
      self.turn_on('input_boolean.easyplus_boiler_heating')
      time.sleep(2)
      boiler=self.get_state('input_boolean.easyplus_boiler_heating')
      self.log("boiler %s", boiler)
      tg = "Boiler is {} ".format(boiler)
      self.call_service("notify/dageraad",message = tg)

    self.call_service("shell_command/heating_"+friendly)
    self.set_state("sensor.notify_message", state="Heating started")
    temp_cur = self.get_state(entity, attribute="current_temperature")
    temp_set = self.get_state(entity, attribute="temperature")
    self.log("climate {} turned on, temperature set to  {}".format(friendly, temp_set))
    self.call_service("notify/dageraad", message = ("climate {} turned on, now {}°C and set to {}°C".format(friendly, temp_cur, temp_set)))

    return

   if old == "heat" and new == "off":
    self.call_service("climate/set_temperature", entity_id = self.args["climate"], temperature = 5)
    self.call_service("shell_command/heating_tmp_"+friendly+"_off")
    self.set_state("sensor.notify_message", state="Heating Completed")
    temp_cur = self.get_state(entity, attribute="current_temperature")
    temp_set = self.get_state(entity, attribute="temperature")
    self.log("climate {} turned off, temperature set to {}".format(friendly, temp_set))
    self.call_service("notify/dageraad", message = ("climate {} turned off, now {}°C and set to {}°C".format(friendly, temp_cur, temp_set)))
    self.set_state("sensor.notify_message", state="Heating {} Completed".format(friendly))
    return
   self.log(self.args)



#old notification
#    current_temp= self.get_state(entity, attribute="current_temperature")
#    heating_temp= self.get_state(entity, attribute="temperature")
#    self.call_service('notify/dageraad',
#        title="[Heating Completed]\n",
#        message=("\n===============\n"
#                 "Room: {}\nCurrent temp: {}°C\nHeating temp: {}°C".format(friendly,current_temp,heating_temp)))
###
#    current_temp= self.get_state(entity, attribute="current_temperature")
#    heating_temp= self.get_state(entity, attribute="temperature")
#    self.call_service('notify/dageraad',
#        title="[Heating Started]\n",
#        message=("\n===============\n"
#                 "Room: {}\nCurrent temp: {}°C\nHeating temp: {}°C".format(friendly,current_temp,heating_temp)))

##Nordine version
  #  if old == "off" and new == "heat":
  #   for i in range (7):
  #     if telnet != 'on':
  #       self.get_state('binary_sensor.easyplus_telnet')
  #       self.turn_off('switch.easyplus')
  #       self.turn_on('switch.easyplus')
  #       time.sleep(25)
  #       self.get_state('binary_sensor.easyplus_telnet')
  #       self.log("Failure - Telnet %s", telnet)
  #       tg = "Failure - Easyplus is {}, Telnet state is {} ".format(easyplus, telnet)
  #       self.call_service("notify/dageraad",message = tg)
  #     else:
  #         break
  #   self.log("Succes - Telnet %s", telnet)
  #   tg = "Succes - Easyplus is {}, Telnet state is {} ".format(easyplus, telnet)
  #   self.call_service("notify/dageraad",message = tg)



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


        # tg = "Easyplus is rebooting Telnet is {} ".format(easyplus)
        # self.call_service("notify/dageraad",message = tg)
