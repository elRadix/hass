import appdaemon.plugins.hass.hassapi as hass
import subprocess
import datetime
import time
class easyplus(hass.Hass):

 def initialize(self):
    self.listen_state(self.error_cb, 'sensor.error')

 def error_cb(self, entity, attribute, old, new, kwargs):
    easyplus = self.get_state('binary_sensor.easyplus_telnet')
    error = "expect -f /opt/scripts/apex.sh " + str(new).split(".sh ",1)[1]
    self.log("{}".format(error))
    for i in range (0, 3, 1):
     if easyplus != 'on':
         self.turn_on('switch.easyplus')
         time.sleep(20)
         easyplus = self.get_state('switch.easyplus')
         self.log("easyplus turned {} for switch to work".format(easyplus))
         self.call_service("notify/dageraad", message = ("easyplus turned {} for switch to work".format(easyplus)))
         break
    cmd = '"' + error + '", shell=True'
    self.log("{}".format(cmd))
    returncode = subprocess.run("expect -f /opt/scripts/apex.sh 'Setrelay 34,1'", shell=True)
    self.log(self.args)