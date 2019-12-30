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
    self.log("{}".format(failed))
   #reboot = []
    while self.get_state('binary_sensor.easyplus_telnet') == 'off':
      # reboot = reboot + 1
      self.turn_off('switch.easyplus')
      time.sleep(2)
      self.turn_on('switch.easyplus')
      tg = "Easyplus is rebooting ".format(failed)
      self.call_service("notify/dageraad",message = tg)
      time.sleep(35)
      telnet = self.get_state('binary_sensor.easyplus_telnet')
      easyplus = self.get_state('switch.easyplus')
      self.get_state('binary_sensor.easyplus_telnet')
      self.log("telnet state is %s", telnet)
      tg = "Easyplus is {}, Telnet is {} ".format(easyplus, telnet)
      self.call_service("notify/dageraad",message = tg)
      returncode = subprocess.run("{} {}".format(script, failed), shell=True, capture_output=True).stdout
      self.log("{} {}".format(script, failed))
      self.call_service("notify/dageraad", message = ("Started Switch: {}".format(failed)))
      self.log(self.args)



   #  if ",0" not in failed:
   #    for i in range (0, 3, 1):
   #     if easyplus != 'on':
   #         self.turn_off('switch.easyplus')
   #         time.sleep(2)
   #         self.turn_on('switch.easyplus')
   #         self.call_service("notify/dageraad", message = ("Run {} - Reboot Easyplus".format(i)))
   #         time.sleep(35)
   #         telnet = self.get_state('binary_sensor.easyplus_telnet')
   #         easyplus = self.get_state('switch.easyplus')
   #         self.log("easyplus {}, telnet {}, loop {}".format(easyplus, telnet, i))
   #         self.call_service("notify/dageraad", message = ("Easyplus is {}, Telnet is {} - loop {}".format(easyplus, telnet, i)))
   #         break
   #    returncode = subprocess.run("{} {}".format(script, failed), shell=True, capture_output=True).stdout
   #    self.log("state: {} {}".format(script, failed))
   #    self.call_service("notify/dageraad", message = ("switch {}".format(easyplus)))
   #    self.log(self.args)






