import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
class easyplus(hass.Hass):

 def initialize(self):
    self.listen_state(self.error_cb, 'sensor.error')

 def error_cb(self, entity, attribute, old, new, kwargs):
    error = self.get_state(entity)
    easyplus = self.get_state('binary_sensor.easyplus_telnet')
    self.log("%s", error)
    mylist = str(error).split(':')
    self.log("list is split, now printing the split list")
    self.log(mylist)
    if error.startswith("Command failed: "):
       return error[17:]
    self.log("%s", error)
    self.log(self.args)
