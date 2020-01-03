import appdaemon.plugins.hass.hassapi as hass
import subprocess
import datetime
import time
import os
class telnet(hass.Hass):

 def initialize(self):
    self.listen_state(self.telnet_cb, 'input_boolean.night')

 def telnet_cb(self, entity, attribute, old, new, kwargs):
    os.chdir('/opt/scripts/') #to get into the directory where app is installed
    process = subprocess.Popen(['/bin/bash', '/opt/scripts/telnet.sh'],
                           shell=True,
                           stdout=subprocess.PIPE,
                           universal_newlines=True)
    while True:
        output = process.stdout.readline()
        print(output.strip())
        # Do something else
        return_code = process.poll()
        if return_code is not None:
            print('OUTPUT =', return_code)
            # Process has finished, read rest of the output
            for output in process.stdout.readlines():
                print(output.strip())
            break


   #  script = "/opt/scripts/telnet.sh"
   #  telnet = subprocess.run(['/bin/bash', '/opt/scripts/telnet.sh'], timeout =6, shell=True, stdout=subprocess.PIPE)
   #  output = telnet.stdout.decode('utf-8')
   #  print(output)
   #  print(telnet.stdout)
   #  self.log("{}".format(telnet))
   #  self.log(self.args)


#  def easyplus_cb(self, entity, attribute, old, new, kwargs):
#     script = "expect -f /opt/scripts/apex.sh"
#     telnet = self.get_state('binary_sensor.easyplus_telnet')
#     easyplus = self.get_state('switch.easyplus')
#     failed = str(new).split(".sh ",1)[1]
#     loop = 0
#     cmdtelnet = "/opt/scripts/telnet.sh"
#     self.log("{}".format(failed))
#     if ",0" not in failed:
#       while self.get_state('binary_sensor.easyplus_telnet') == 'off' and loop <=4:
#          loop+=1
#          self.call_service("notify/dageraad", message = ("Failed switch: {}".format(failed, )))
#          self.turn_off('switch.easyplus')
#          time.sleep(2)
#          self.turn_on('switch.easyplus')
#          time.sleep(35)
#          telnet = self.get_state('binary_sensor.easyplus_telnet')
#          easyplus = self.get_state('binary_sensor.easyplus_telnet')
#          self.log("telnet state %s", telnet)
#          self.log("easyplus {} and telnet {} - restart #{}".format(easyplus, telnet, loop))
#          self.call_service("notify/dageraad", message = ("easyplus {} and telnet {} - restart #{}".format(easyplus, telnet, loop)))
#       else:
#          if self.get_state('binary_sensor.easyplus_telnet') == 'off' and loop >3:
#            self.log("Easyplud failed after {} tries, telnet is {} ".format(loop, telnet))
#            self.call_service("notify/dageraad", message = ("Easyplus failed after {} tries, telnet still {} ".format(loop, telnet)))
#          if self.get_state('binary_sensor.easyplus_telnet') == 'on' and loop <=3:
#            returncode = subprocess.run("{} {}".format(script, failed), shell=True, capture_output=True).stdout
#            self.log("{} {}".format(script, failed))
#            self.call_service("notify/dageraad", message = ("switch turned {} succesfully".format(easyplus)))
#            self.set_state("sensor.error", state=".sh '0,0'")
#            process = subprocess.Popen(cmdtelnet, shell=True, stdout=subprocess.PIPE)
#            process.wait()
#            print (process.returncode)
#       self.log(self.args)