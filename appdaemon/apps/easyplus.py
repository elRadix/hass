import appdaemon.plugins.hass.hassapi as hass
import subprocess
import datetime
import time
class easyplus(hass.Hass):

 def initialize(self):
    self.listen_state(self.failed_cb, 'sensor.error')

 def failed_cb(self, entity, attribute, old, new, kwargs):
    script = "expect -f /opt/scripts/apex.sh"
    telnet = self.get_state('binary_sensor.easyplus_telnet')
    easyplus = self.get_state('switch.easyplus')
    failed = str(new).split(".sh ",1)[1]
    loop = 0
    self.log("{}".format(failed))
    if ",0" not in failed:
      while self.get_state('binary_sensor.easyplus_telnet') == 'off' and loop <=4:
         loop+=1
         self.turn_off('switch.easyplus')
         time.sleep(2)
         self.turn_on('switch.easyplus')
         time.sleep(35)
         telnet = self.get_state('binary_sensor.easyplus_telnet')
         easyplus = self.get_state('binary_sensor.easyplus_telnet')
         self.log("telnet state %s", telnet)
         self.log("easyplus {} and telnet {} to enable switch - restart #{}".format(easyplus, telnet, loop))
         self.set_state("sensor.error", state=".sh '0,0'")
         self.call_service("notify/dageraad", message = ("easyplus turned {} to enable switch, restart #{}".format(easyplus, loop)))
         if self.get_state('binary_sensor.easyplus_telnet') == 'off' and loop == 4:
           self.log("Reboot failed after {} tries, telnet is {} ".format(loop, telnet))
           self.call_service("notify/dageraad", message = ("Reboot failed after {} tries, telnet still {} ".format(loop, telnet)))
      returncode = subprocess.run("{} {}".format(script, failed), shell=True, capture_output=True).stdout
      self.log("{} {}".format(script, failed))
      self.call_service("notify/dageraad", message = ("switch turned {} succesfully".format(easyplus)))
      self.log(self.args)


