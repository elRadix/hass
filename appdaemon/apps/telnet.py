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
 #   telnet = subprocess.call(['/opt/scripts/telnet.py'])
    process = subprocess.Popen(['python', '/opt/scripts/telnet.py'],
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