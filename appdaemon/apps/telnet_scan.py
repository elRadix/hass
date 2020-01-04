import appdaemon.plugins.hass.hassapi as hass
import datetime
import telnetlib
import time
import re

class TelnetEasyplus(hass.Hass):

  def initialize(self):
    #Run callback to run get_bands every 30s starting now
    self.run_every(self.get_easyplus, self.datetime(), 30)

  def get_easyplus(self, kwargs):
    self.log("getting easyplus log...")
    tn = telnetlib.Telnet("192.168.3.61",2024)
    tn.write("pass apex\r\n".encode())
    time.sleep(0.5)
    tn.write("getdata\r\n".encode())
    time.sleep(0.5)
    data=tn.read_very_eager()
    #sys.stdout.write(data)
    tn.close()
    self.log(data)

    #data2=re.findall(r'LTE band: *(\S*)', data.decode())
    #self.set_state("input_text.band", state = data2 ) #BCK - need to parse data2