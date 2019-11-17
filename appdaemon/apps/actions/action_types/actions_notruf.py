import appdaemon.plugins.hass.hassapi as hass
import datetime
import tempfile
import subprocess
import time

class actions_notruf(hass.Hass):

    def initialize(self):
        return


    def action(self, kwargs):
        self.log("A NOTRUF HAS BEEN CALLED!!!")
        cmd = [self.app_config["settings"]["dirs"]["alexa_media_dir"] + "/" + self.app_config["settings"]["files"]["alexa"],"-lastalexa"]
        with tempfile.TemporaryFile() as f:
            self.subprocessresult = subprocess.Popen(cmd, stdin=None, stdout=subprocess.PIPE, stderr=f)   
            out,err = self.subprocessresult.communicate()
            if out != None:
                state = out.decode("utf-8").strip()
                self.message = "achtung achtung achtung, da ist ein notruf im " + state
            else:
                self.message = "achtung achtung achtung, da ist ein notruf aber ich kan nicht sagen wo er herkommt"
            self.let_alexa_speak_notruf(self)

    def let_alexa_speak_notruf(self,kwargs):
        while self.get_state("switch.notruf") != "on":
            self.log("CALLED FOR HELP")
            self.set_state("sensor.nofify_message", state = "alexa;(all){}".format(message))
            time.sleep(30)  
