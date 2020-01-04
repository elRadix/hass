import appdaemon.plugins.hass.hassapi as hass
import datetime
import telnetlib
import time
import re

class telnet_scan(hass.Hass):



 def initialize(self):
    self.listen_state(self.get_easyplus, 'input_boolean.night')

 def get_easyplus(self, kwargs):
    self.log("getting easyplus log...")
    tn = telnetlib.Telnet("192.168.3.61",2024)
    tn.write("pass apex\r\n".encode())
    time.sleep(0.5)
    tn.write("getdata\r\n".encode())
    time.sleep(3)
    data=tn.read_very_eager()
    #sys.stdout.write(data)
    tn.close()
    self.log(data)

    #data2=re.findall(r'LTE band: *(\S*)', data.decode())
    #self.set_state("input_text.band", state = data2 ) #BCK - need to parse data2



#   def initialize(self):
#     #Run callback to run get_bands every 30s starting now
#     # self.run_every(self.get_easyplus, datetime.datetime.now(),5)
#     runtime = datetime.datetime.now()
#     addseconds = (round((runtime.minute*60 + runtime.second)/300)+1)*300
#     runtime = runtime.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(seconds=addseconds)
#     self.run_every(self.get_easyplus,runtime,1)
