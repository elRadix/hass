import appdaemon.plugins.hass.hassapi as hass
import subprocess
import datetime
import time
class easyplus(hass.Hass):

 def initialize(self):
    self.listen_state(self.error_cb, 'sensor.error')

 def error_cb(self, entity, attribute, old, new, kwargs):
    easyplus = self.get_state('binary_sensor.easyplus_telnet')
    error = "['/usr/bin/expect', '-f', '"+str(new).split("-f ",1)[1]+",shell=True']"
#    error = "[/usr/bin/expect -f "+str(new).split("-f ",1)[1]+",shell=True]"

    self.log("{}".format(error))
    for i in range (0, 3, 1):
     if easyplus != 'on':
#         self.turn_off('switch.easyplus')
         self.turn_on('switch.easyplus')
         time.sleep(20)
         easyplus = self.get_state('switch.easyplus')
         self.log("easyplus turned {} for switch to work".format(easyplus))
         self.call_service("notify/dageraad", message = ("easyplus turned {} for switch to work".format(easyplus)))
         break
    cmd = str(error)
    subprocess.call([cmd])
    subprocess.call(["ls", "-l"])
    self.log("{}".format(cmd))
    self.log("{}".format(error))
    self.log(self.args)
