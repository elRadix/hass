import appdaemon.plugins.hass.hassapi as hass
import datetime
import telnetlib
import time
import re
import time

class telnet_scan(hass.Hass):

#  def initialize(self):
# #    time = datetime.time(0, 0, 0)
#     self.listen_state(self.get_easyplus, 'input_boolean.night')
# #    self.handle = self.run_every(get_easyplus, time)


 def initialize(self):
    self.listen_state(self.get_easyplus, 'input_boolean.night_late')



 def get_easyplus(self):
    self.log("getting easyplus log...")
    tn = telnetlib.Telnet("192.168.3.61",2024)
    tn.write("pass apex\r\n".encode())
    while self.get_state('binary_sensor.easyplus_telnet') == 'on':
      self.log("getting easyplus log...")
      data=tn.read_very_eager()
      #tn.close()
      self.log(data)
      if "DigitalOut 33,ON".encode() in data:
         self.log("Microwave ON")
         self.set_state("switch.stp_keuken_microgolf", state = "on")
      if "DigitalOut 33,OFF".encode() in data:
         self.log("Microwave OFF")
         self.set_state("switch.stp_keuken_microgolf", state = "off")
    self.log(self.args)



#  def get_easyplus(self, entity, attribute, old, new, kwargs):
#     self.log("getting easyplus log...")
#     tn = telnetlib.Telnet("192.168.3.61",2024)
#     tn.write("pass apex\r\n".encode())
#     time.sleep(0.5)
#     tn.write("getdata\r\n".encode())
#     time.sleep(0.5)
#     data=tn.read_very_eager()
#     tn.close()
#     self.log(data)

    #tn.read_until("b".encode())
    #data=tn.read_very_eager()
#    data = tn.read_all() #(‘ascii’)

    #data2=re.findall(r'LTE band: *(\S*)', data.decode())
    #self.set_state("input_text.band", state = data2 ) #BCK - need to parse data2


#  def initialize(self):
    # self.listen_state(self.get_easyplus, 'input_boolean.night')
#   def initialize(self):
#     #Run callback to run get_bands every 30s starting now
#     # self.run_every(self.get_easyplus, datetime.datetime.now(),5)
#     runtime = datetime.datetime.now()
#     addseconds = (round((runtime.minute*60 + runtime.second)/300)+1)*300
#     runtime = runtime.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(seconds=addseconds)
#     self.run_every(self.get_easyplus,runtime,1)
