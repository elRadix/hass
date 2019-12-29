import appdaemon.plugins.hass.hassapi as hass
import subprocess
import datetime
import time
class easyplus(hass.Hass):

 def initialize(self):
    self.listen_state(self.failed_cb, 'sensor.error')

 def failed_cb(self, entity, attribute, old, new, kwargs):
    script = "expect -f /home/homeassistant/.homeassistant/opt/bin/apex.sh"
    easyplus = self.get_state('binary_sensor.easyplus_telnet')
    failed = str(new).split(".sh ",1)[1]
    self.log("{}".format(failed))
    if ",0" not in failed:
      for i in range (0, 3, 1):
       if easyplus != 'on':
           self.turn_off('switch.easyplus')
           self.turn_on('switch.easyplus')
           time.sleep(30)
           easyplus = self.get_state('binary_sensor.easyplus_telnet')
           self.log("easyplus {}, loop: {}".format(easyplus, i))
           self.call_service("notify/dageraad", message = ("easyplus {}, loop {}".format(easyplus, i)))
           break 
      returncode = subprocess.run("{} {}".format(script, failed), shell=True, capture_output=True).stdout
      self.log("state: {} {}".format(script, failed))
      self.call_service("notify/dageraad", message = ("switch {}".format(easyplus)))
      self.log(self.args)

