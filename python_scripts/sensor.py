def initialise(...):
  self.listen_state(self.change_state,self.args["main_sensor"])
  for sensor in self.args["attributes"]: 
    self.listen_state(self.change_state,sensor)

def change_state(...):
  all_attributes = {}
  statevalue = self.get_state(self.args["main_sensor"])
  for name,sensor in self.args["attributes"].items():
    all_attributes[name] = self.get_state(sensor)
  self.set_state(self.args["new_sensor_name"], state=statevalue,attributes=all_attributes)