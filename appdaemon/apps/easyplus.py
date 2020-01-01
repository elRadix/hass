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
      while self.get_state('binary_sensor.easyplus_telnet') == 'off' and loop != 4:
         loop+=1
         self.turn_off('switch.easyplus')
         time.sleep(2)
         self.turn_on('switch.easyplus')
         time.sleep(35)
         telnet = self.get_state('binary_sensor.easyplus_telnet')
         easyplus = self.get_state('binary_sensor.easyplus_telnet')
         self.log("telnet state %s", telnet)
         self.log("easyplus {} and telnet {} to enable switch - restart {}".format(easyplus, telnet, i))
         self.call_service("notify/dageraad", message = ("easyplus turned {} an to enable switch - restart {}".format(easyplus, telnet, i)))
         break
      returncode = subprocess.run("{} {}".format(script, failed), shell=True, capture_output=True).stdout
      self.log("{} {}".format(script, failed))
      self.call_service("notify/dageraad", message = ("switch turned {} succesfully".format(easyplus)))
      self.log(self.args)



   #  failed = str(new).split(".sh ",1)[1]
   #  self.log("{}".format(failed))
   #  if ",0" not in failed:
   #    while self.get_state('binary_sensor.easyplus_telnet') == 'off':
   #       for i in range (0, 3, 1):
   #            self.turn_off('switch.easyplus')
   #            time.sleep(1)
   #            self.turn_on('switch.easyplus')
   #            time.sleep(35)
   #            telnet = self.get_state('binary_sensor.easyplus_telnet')
   #            easyplus = self.get_state('binary_sensor.easyplus_telnet')
   #            self.log("telnet state %s", telnet)
   #            self.log("easyplus turned {} to enable switch - restart {}".format(easyplus, i))
   #            self.call_service("notify/merwone", message = ("easyplus turned {} to enable switch - restart {}".format(easyplus, i)))
   #            break
   #    returncode = subprocess.run("{} {}".format(script, failed), shell=True, capture_output=True).stdout
   #    self.log("{} {}".format(script, failed))
   #    self.call_service("notify/merwone", message = ("switch turned {} succesfully".format(easyplus)))
   #    self.log(self.args)




#  def failed_cb(self, entity, attribute, old, new, kwargs):
#     script = "expect -f /opt/scripts/apex.sh"
#     telnet = self.get_state('binary_sensor.easyplus_telnet')
#     easyplus = self.get_state('switch.easyplus')
#     failed = str(new).split(".sh ",1)[1]
#     self.log("{}".format(failed))
   #  loop = 0
   #  while self.get_state('binary_sensor.easyplus_telnet') == 'off' or loop != 3:
   #    loop+=1
#       self.turn_off('switch.easyplus')
#       time.sleep(2)
#       self.turn_on('switch.easyplus')
#       self.call_service("notify/dageraad", message = ("Easyplus Reboot, try nr {} ".format(loop)))
#       time.sleep(35)
#       telnet = self.get_state('binary_sensor.easyplus_telnet')
#       easyplus = self.get_state('switch.easyplus')
#       self.get_state('binary_sensor.easyplus_telnet')
#       self.log("telnet state is %s", telnet)
#       self.call_service("notify/dageraad", message = ("Easyplus is {}, Telnet is {}".format(easyplus, telnet)))
#       returncode = subprocess.run("{} {}".format(script, failed), shell=True, capture_output=True).stdout
#       self.log("{} {}".format(script, failed))
#       self.call_service("notify/dageraad", message = ("Started Switch {} after {} tries  ".format(failed, loop)))
#       self.log(self.args)


    loop = 0
    while self.get_state('binary_sensor.easyplus_telnet') == 'off' or loop = 3:
      loop+=1