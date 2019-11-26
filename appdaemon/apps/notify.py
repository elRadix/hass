import appdaemon.appapi as appapi

class notify(appapi.AppDaemon):

  def initialize(self):
    self.set_state("sensor.notify_message",state=" ")
    self.listen_state(self.send_notify,"sensor.notify_message")

#   def send_notify(self, entity, attribute, old, new, kwargs):
#     self.log("Updated Sensor reading - Value : " + new)
#     self.call_service('notify/dageraad', message=new)


  def send_notify(self, entity, attribute, old, new, kwargs):
    self.log("Updated Sensor value : " + new)
    self.call_service('notify/dageraad', message=new)

    ha_trigger = self.get_state("sensor.notify_message","frontend")
    self.log("Frontend value : {}".format(ha_trigger))

    if ha_trigger:
        self.call_service('persistent_notification/create',
            title="Attention", message=new+ " - " + datetime.now().strftime('@ %-I:%M %p') )