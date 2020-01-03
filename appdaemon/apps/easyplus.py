import appdaemon.plugins.hass.hassapi as hass
import subprocess
import datetime
import time
class easyplus(hass.Hass):

 def initialize(self):
    self.listen_state(self.easyplus_cb, 'sensor.error')

 def easyplus_cb(self, entity, attribute, old, new, kwargs):
    script = "expect -f /opt/scripts/apex.sh"
    telnet = self.get_state('binary_sensor.easyplus_telnet')
    easyplus = self.get_state('switch.easyplus')
    failed = str(new).split(".sh ",1)[1]
    loop = 0
    self.log("{}".format(failed))
    if ",0" not in failed:
      while self.get_state('binary_sensor.easyplus_telnet') == 'off' and loop <=4:
         loop+=1
         self.call_service("notify/dageraad", message = ("Failed switch: {}".format(failed, )))
         self.turn_off('switch.easyplus')
         time.sleep(2)
         self.turn_on('switch.easyplus')
         time.sleep(35)
         telnet = self.get_state('binary_sensor.easyplus_telnet')
         easyplus = self.get_state('binary_sensor.easyplus_telnet')
         self.log("telnet state %s", telnet)
         self.log("easyplus {} and telnet {} - restart #{}".format(easyplus, telnet, loop))
         self.call_service("notify/dageraad", message = ("easyplus {} and telnet {} - restart #{}".format(easyplus, telnet, loop)))
      else:
         if self.get_state('binary_sensor.easyplus_telnet') == 'off' and loop >3:
           self.log("Easyplud failed after {} tries, telnet is {} ".format(loop, telnet))
           self.call_service("notify/dageraad", message = ("Easyplus failed after {} tries, telnet still {} ".format(loop, telnet)))
         if self.get_state('binary_sensor.easyplus_telnet') == 'on' and loop <=3:
           returncode = subprocess.run("{} {}".format(script, failed), shell=True, capture_output=True).stdout
           for returncode in proc.stdout.split('\n'):
             print(returncode)
           self.log("{} {}".format(script, failed))
           self.call_service("notify/dageraad", message = ("switch turned {} succesfully".format(easyplus)))
           self.set_state("sensor.error", state=".sh '0,0'")
      self.log(self.args)




# proc = subprocess.run(['wmctrl', '-l'], encoding='utf-8', stdout=subprocess.PIPE)
# for line in proc.stdout.split('\n'):
#     print(line)

#  def failed_cb(self, entity, attribute, old, new, kwargs):
#     script = "expect -f /home/homeassistant/.homeassistant/opt/bin/apex.sh"
#     failed = str(new).split(".sh ",1)[1]
#     loop = 0
#     self.log("{}".format(failed))
#     if ",0" not in failed:
#       while self.get_state('binary_sensor.easyplus_telnet') == 'off' and loop <=2:
#         loop += 1
#         self.turn_off('switch.easyplus')
#         time.sleep(1)
#         self.turn_on('switch.easyplus')
#         time.sleep(35)
#         telnet = self.get_state('binary_sensor.easyplus_telnet')
#         easyplus = self.get_state('binary_sensor.easyplus_telnet')
#         self.log("telnet state %s", telnet)
#         self.log("easyplus turned {} to enable switch - restart {}".format(easyplus, loop))
#         self.call_service("notify/merwone", message = ("easyplus turned {} to enable switch - restart {}".format(easyplus, loop)))
#       else:
#         if self.get_state('binary_sensor.easyplus_telnet') == 'off' and loop >2:
#           self.log("easyplus failed to turn on - restart {}".format(loop))
#           self.call_service("notify/merwone", message = ("easyplus failed to turn on - restart {}".format(loop)))
#         if self.get_state('binary_sensor.easyplus_telnet') == 'on' and loop <=2:
#           returncode = subprocess.run("{} {}".format(script, failed), shell=True, capture_output=True).stdout
#           self.log("{} {}".format(script, failed))
#           self.call_service("notify/merwone", message = ("switch turned {} succesfully".format(easyplus)))
#           self.set_state("sensor.error", state=".sh '0,0'")
#     self.log(self.args)
