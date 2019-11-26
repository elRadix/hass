import appdaemon.appapi as appapi

class notify(appapi.AppDaemon):

  def initialize(self):
    self.set_state("sensor.notify_message",state=" ")
    self.listen_state(self.send_notify,"sensor.notify_message")

  def send_notify(self, entity, attribute, old, new, kwargs):
    self.log("Updated Sensor reading - Value : " + new)
    self.call_service('notify/dageraad',message = new)
