import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
class easyplus(hass.Hass):

 def initialize(self):
   self.listen_state(self.easyplus_cb, self.args["entity"])

 def easyplus_cb(self, entity, attribute, old, new, kwargs):
   friendly = self.get_state(entity, attribute="friendly_name")
   state = self.get_state(entity)
   easyplus = self.get_state('binary_sensor.easyplus_telnet')
   self.log("%s %s", friendly, state)
   if old != "on" and new != "off":
    if easyplus != 'on':
      for i in range (3):
        self.turn_off('switch.easyplus')
        self.turn_on('switch.easyplus')
        time.sleep(10)
        self.log("easyplus %s", easyplus)
        self.turn_off(entity)
        self.turn_on(entity)
        self.log("%s %s", friendly, state)
    return
    self.log(self.args)


# class opentherm_OTGW(hass.Hass):

#     def initialize(self):

#         #In this function the you need to set the ip and the port used by the OTGW, after that it trys to connect and validate the paramters. Otherwise it throws an error.

#         self.HOST = "192.168.1.61" #set OTGW ip
#         self.PORT = "2024" #set OTGW port
#         self.EASYPLUS = telnetlib.Telnet() #telnet object self.OTGW
#         self.log_level = 1 #set to 0 to supress logs in functions
#         self.validation = 0 #used to stop function if except thrown

#         try:
#             self.log("Testing connection")
#             self.EASYPLUS.open(self.HOST,self.PORT,1)
#             self.EASYPLUS.close()
#             self.validation = 1
#             self.log("Connection successful")
#             self.log("EASYPLUS is ready")

#         except:
#             self.error("Connection couldn't establish, HOST and PORT set ?")
#             self.error("Opentherm is not working")
#             self.validation = 0


#         self.control_setpoint_old = 0 
#         self.data_list_old = 0
#         self.data_list = 0


#         if self.validation == 1:

#             self.run_every(self.run_opentherm,datetime.now(),20)