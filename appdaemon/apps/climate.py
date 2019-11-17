import appdaemon.plugins.hass.hassapi as hass
import time
class climate(hass.Hass):

 def initialize(self):
   for climate in self.args["entities"]:
     self.listen_state(self.climate_cb, climate, attribute='state')
     self.log(self.args)
 def climate_cb(self, entity, attribute, old, new, kwargs):
   if old == "off" and new == "heat":
    self.log((entity, attribute, old, new, kwargs))
    if self.get_state('switch.easyplus', attribute='state') != 'on':
      self.turn_on('switch.easyplus')
      self.log("easyplus on")
      time.sleep(20)
    if self.get_state('input_boolean.easyplus_boiler_heating', attribute='state') != 'on':
      self.turn_on('input_boolean.easyplus_boiler_heating')
      self.log("boiler on")
    self.call_service("shell_command/heating_living")
    self.call_service("shell_command/heating_eetkamer")
    self.call_service("shell_command/heating_floradix")
    self.call_service("shell_command/heating_sara")
    self.call_service("shell_command/heating_yassin")
    self.log("ON setpoint sent")
    return
   if old == "heat" and new == "off":
    self.call_service("shell_command/heating_tmp_living_off")
    self.call_service('climate/set_temperature', entity_id=climate.living, temperature=5)
    self.call_service("shell_command/heating_tmp_eetkamer_off")
    self.call_service("shell_command/heating_tmp_slp1_off")
    self.call_service('climate/set_temperature', entity_id=climate.floradix, temperature=5)
    self.call_service("shell_command/heating_tmp_slp2_off")
    self.call_service("shell_command/heating_tmp_slp3_off")
    self.call_service("shell_command/heating_tmp_eetkamer_off")
    self.log("OFF setpoint sent")
    return