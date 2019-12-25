import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
class easyplus(hass.Hass):

 def initialize(self):
    self.listen_state(self.error_cb, 'sensor.error')

 def error_cb(self, entity, attribute, old, new, kwargs):
    easyplus = self.get_state('binary_sensor.easyplus_telnet')
    for i in range (0, 3, 1):
     if easyplus != 'on':
#         self.turn_off('switch.easyplus')
         self.turn_on('switch.easyplus')
         time.sleep(20)
         easyplus = self.get_state('switch.easyplus')
         self.log("easyplus turned {} for switch to work".format(easyplus))
           break
    error = str(new).split(":",1)[1]
    cmd = ['error']
    returncode = subprocess.call(cmd)
    self.log("{}".format(error))
    self.log(self.args)



