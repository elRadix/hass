#
# this app is the base app for creating actions in yaml.
# actions is something like the home assistant automations, but it can be translated
# to an understandable workflow in your own words.
# a basic example without translation:
#
#   if:
#     sensor.telefoon: {"new_state": "idle", "delay": 30}
#   do_first:
#     - input_boolean.woonkamer_tv_pause: {"value": "off"}
#     - sensor.tv_tijdelijk_pause: {"value": "off"}
#   do_after_some_delay:
#     - input_boolean.woonkamer_tv_pause: {"value": "on"}
#     - sensor.tv_tijdelijk_pause: {"value": "on"}
#   hold_for:
#     sensor.tv_tijdelijk_pause: "off"
#     input_boolean.woonkamer_tv: "off"
#
# you can translate that and for example do it in dutch:
#
#   als:
#     sensor.telefoon: {"nieuwe_waarde": "idle", "pauze": 30}
#   doe_dan_eerst:
#     - input_boolean.woonkamer_tv_pause: {"waarde": "off"}
#     - sensor.tv_tijdelijk_pause: {"waarde": "off"}
#   na_de_pauze:
#     - input_boolean.woonkamer_tv_pause: {"waarde": "on"}
#     - sensor.tv_tijdelijk_pause: {"waarde": "on"}
#   doe_het_niet_als:
#     sensor.tv_tijdelijk_pause: "off"
#     input_boolean.woonkamer_tv: "off"
#
# you can put in delays for every action.
# you can use several special values (see the sanitize function in the helpers app)
# you can trigger the automations based on time, sunset, sunrise, state change
# you can put the automations in a google calendar (and even schedule everything there)
#



import appdaemon.plugins.hass.hassapi as hass
import datetime
import yaml

class actions(hass.Hass):

  def initialize(self):
    #########################################################################################
    # lets start by seeing if we need to translate:
    #########################################################################################
    if "language" in self.args:
      self.language = self.app_config["actions_language_" + self.args["language"]]
      self.language_name = self.args["language"]
    else:
      self.language = self.app_config["actions_language_default"]
      self.language_name = "default"
    #########################################################################################
    # setup variables
    #########################################################################################
    actualtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.special_element_types = [self.language["sunset"],self.language["sunrise"],self.language["time"],self.language["location"],self.language["hourly"]]
    self.action = self.args
    #########################################################################################
    # initialise the handle
    #########################################################################################
    self.timer_running = None
    #########################################################################################
    # keep track of the active action (because handle doesnt get reset to None)
    #########################################################################################
    self.active_action = None
    #########################################################################################
    # check if we want logging (for debugging)
    #########################################################################################
    self.debug_logging = False
    if self.language["debug_logging"] in self.action:
      if self.action[self.language["debug_logging"]]:
        self.debug_logging = True
    #########################################################################################
    # check if we want action logging (default = True)
    #########################################################################################
    self.action_logging = True
    if self.language["no_action_log"] in self.action:
      if self.action[self.language["no_action_log"]]:
        self.action_logging = False
    #########################################################################################
    # register our custom constraint function
    #########################################################################################
    if self.language["hold_for"] in self.action:
      constraint_conditions = self.action[self.language["hold_for"]]
    else:
      constraint_conditions = {"no_hold": ""}
    self.register_constraint("custom_constraint")

    if self.language["if"] in self.action:
      #########################################################################################
      # there is a ifstatement, so set it up
      #########################################################################################
      if_statements = self.action[self.language["if"]]
      for statements in if_statements:
        for element,conditions in statements.items():
          #########################################################################################
          # split up the iff statement into usable variables
          #########################################################################################
          type, entity_name, time_to_action2, offset, start_time, start_time_set, new_state, old_state, attribute, use_new_state, use_old_state, use_attribute = self.split_if_statement(element, conditions)
          #########################################################################################
          # if it is a sunset/sunrise type create a run_at_sunrise/sunset 
          #########################################################################################
          if type == self.language["sunset"]:
            self.run_at_sunset(self.preaction1, offset = offset, custom_constraint = constraint_conditions, entityname = entity_name ,time_till_action2 = time_to_action2, if_conditions=statements)
          elif type == self.language["sunrise"]:
            self.run_at_sunrise(self.preaction1, offset = offset, custom_constraint = constraint_conditions, entityname = entity_name ,time_till_action2 = time_to_action2, if_conditions=statements)
          #########################################################################################
          # if it is a time type create a run_daily 
          #########################################################################################
          elif type == self.language["time"]:
            if start_time_set:
              self.run_daily(self.preaction1, start_time, custom_constraint = constraint_conditions, entityname = entity_name, time_till_action2 = time_to_action2, if_conditions=statements)
            else:
              self.log("A time condition (if) needs a start time", "WARNING")
          #########################################################################################
          # if it is a hourly type create a run_hourly 
          #########################################################################################
          elif type == self.language["hourly"]:
            runtime = datetime.time(12, conditions["minutes"], conditions["seconds"])
            self.run_hourly(self.preaction1, runtime, custom_constraint = constraint_conditions, entityname = entity_name, time_till_action2 = time_to_action2, if_conditions=statements)
          #########################################################################################
          # if it is a state type create a listen_state 
          #########################################################################################
          elif not type in self.special_element_types:
            #use_new_state = False
            #use_old_state = False
            #if self.language["new_state"] in conditions:
            #  use_new_state = True
            #if self.language["old_state"] in conditions:
            #  use_old_state = True
            if use_new_state and use_old_state and use_attribute:
              self.listen_state(self.preaction2, element, new = new_state, old = old_state, attribute = attribute, custom_constraint = constraint_conditions, time_till_action2 = time_to_action2, if_conditions=statements)
            elif use_new_state and use_old_state:
              self.listen_state(self.preaction2, element, new = new_state, old = old_state, custom_constraint = constraint_conditions, time_till_action2 = time_to_action2, if_conditions=statements)
            elif use_new_state and use_attribute:
              self.listen_state(self.preaction2, element, new = new_state, attribute = attribute, custom_constraint = constraint_conditions, time_till_action2 = time_to_action2, if_conditions=statements)
            elif use_old_state and use_attribute:
              self.listen_state(self.preaction2, element, old = old_state, attribute = attribute, custom_constraint = constraint_conditions, time_till_action2 = time_to_action2, if_conditions=statements)
            elif use_new_state:
              self.listen_state(self.preaction2, element, new = new_state, custom_constraint = constraint_conditions, time_till_action2 = time_to_action2, if_conditions=statements)
            elif use_old_state:
              self.listen_state(self.preaction2, element, old = old_state, custom_constraint = constraint_conditions, time_till_action2 = time_to_action2, if_conditions=statements)
            else:
              self.listen_state(self.preaction2, element, custom_constraint = constraint_conditions, time_till_action2 = time_to_action2, if_conditions=statements)

    elif self.language["calendar"] in self.action:
      #########################################################################################
      # there is a calendar, so set it up
      #########################################################################################
      #########################################################################################
      # find out which calendar
      #########################################################################################
      calendar = self.action[self.language["calendar"]] 
      #########################################################################################
      # initialise calendar handler
      #########################################################################################
      self.calendar_timer = None
      #########################################################################################
      # set_start_time
      #########################################################################################
      run_gc_check = datetime.time(10, 0, 30)
      #########################################################################################
      # check every minute if the calendar has been update
      #########################################################################################
      self.run_minutely(self.check_calendar, run_gc_check, calendar = calendar)
      #########################################################################################
      # check now if there is an action in calendar
      #########################################################################################
      self.run_in(self.check_calendar,0,calendar = calendar)


  def check_calendar(self, kwargs):
    #########################################################################################
    # check if there is a starttime for the calendar and what message it contains
    #########################################################################################
    next_calendar_action_start_time_str = self.get_state(kwargs["calendar"], attribute = "start_time")
    message = self.get_state(kwargs["calendar"], attribute = "message")
    action = self.get_state(kwargs["calendar"], attribute = "description")
    if message != self.language["action"]:
      #########################################################################################
      # it is something else then an action in the calendar, so stop
      #########################################################################################
      return
    if next_calendar_action_start_time_str == None:
      #########################################################################################
      # there is no future action in the calendar, so stop
      #########################################################################################
      return
    #########################################################################################
    # we have a start time so convert it to a time
    #########################################################################################
    next_calendar_action_start_time = datetime.datetime.strptime(next_calendar_action_start_time_str,"%Y-%m-%d %H:%M:%S")
    if datetime.datetime.now() > next_call:
      #########################################################################################
      # start time is in the past (probably an action thats already started, so stop
      #########################################################################################
      return
    if self.calendar_timer != None:
      #########################################################################################
      # there is already a next action set. cancel it
      #########################################################################################
      self.cancel_timer(self.calendar_timer)
    #########################################################################################
    # there is a valid action so overwrite what we had for action and initialise action
    #########################################################################################
    self.action = yaml.load(action)
    if not self.language["delay"] in self.action:
      #########################################################################################
      # if no delay set, then set it to default 0
      #########################################################################################
      self.action[self.language["delay"]] = 0
    #########################################################################################
    # if there are constraints get them from the action
    #########################################################################################
    if self.language["hold_for"] in self.action:
      constraint_conditions = self.action[self.language["hold_for"]]
    else:
      constraint_conditions = {"no_hold": ""}
    #########################################################################################
    # schedule the action
    #########################################################################################
    self.calendar_timer = self.run_at(self.preaction1, next_calendar_action_start_time, custom_constraint = constraint_conditions, entityname = "time", time_till_action2 = self.action["delay"], if_conditions = {self.language["hold_for"]: {self.language["start"]: next_calendar_action_start_time_str,self.language["delay"]: self.action["delay"]}})
 

  def preaction1(self,kwargs):
    #########################################################################################
    # sunset, sunrise, time and calendar need this kind of callback, send the info forward to action
    #########################################################################################
    self.actiondef(kwargs["entityname"], kwargs["time_till_action2"], kwargs["if_conditions"], "")

  def preaction2(self, entity, attribute, old, new, kwargs):
    #########################################################################################
    # listen_state needs this kind of callback, send the info forward to action
    #########################################################################################
    self.actiondef(entity, kwargs["time_till_action2"], kwargs["if_conditions"], new)

  def actiondef(self, entity, time_till_action2, if_conditions, new):
    #########################################################################################
    # all actions and up here
    # check if there was already a timer running
    # if not start a timer for action 2 (do_after_some_delay) and start action 1 (do_first)
    # if so restart action 2 (do_after_some_delay)
    #########################################################################################
    action1 = False
    action2 = False
    if self.language["do_first"] in self.action:
      action_settings1 = self.action[self.language["do_first"]]
      action1 = True
      reset_after_action = "action1"
    if self.language["do_after_some_delay"] in self.action:
      action_settings2 = self.action[self.language["do_after_some_delay"]]
      action2 = True
      reset_after_action = "action2"
    if self.active_action == None:
      self.active_action = "action started"
      if action1:
        self.debug_log("{} start action1 with entity {}".format(self.name,entity))
        self.run_in(self.do_action, 0, action_settings = action_settings1, action = "action1", reset_after_action = reset_after_action)
      if action2:
        self.debug_log("{} set action2 in delay for {} seconds with entity {}".format(self.name,time_till_action2,entity))
        self.timer_running = self.run_in(self.do_action, time_till_action2, action_settings = action_settings2, action = "action2", reset_after_action = reset_after_action)
      logtype = self.language["if"]
    else:
      if action2:
        self.debug_log("{} restart action2 with entity {}".format(self.name,entity))
        self.cancel_timer(self.timer_running)
        logtype = self.language["if again"]
        self.timer_running = self.run_in(self.do_action, time_till_action2, action_settings = action_settings2, action = "action2", reset_after_action = reset_after_action)
      else:
        self.debug_log("{} action 1 got retriggered by entity {}".format(self.name, entity))
        return
    ####################################################################################
    # log what triggered the action
    ####################################################################################
    if self.language["offset"] in if_conditions[entity]:
      self.run_in(self.action_log, 0, entity = entity, value = if_conditions[entity][self.language["offset"]], type = logtype)
    elif self.language["start"] in if_conditions[entity]:
      self.run_in(self.action_log, 0, entity = entity, value = if_conditions[entity][self.language["start"]], type = logtype)
    else:
      self.run_in(self.action_log, 0, entity = entity, value = new, type = logtype)

  ####################################################################################
  # here we check all actions and trigger the function that does the actual action
  ####################################################################################
  def do_action(self, kwargs):
    self.active_action = kwargs["action"]
    self.debug_log("{} {} started".format(self.name,self.active_action))
    if self.active_action == kwargs["reset_after_action"]:
      self.debug_log("{} stopped after {}".format(self.name,self.active_action))
      self.active_action = None
      self.timer_running = None
    else:
      self.debug_log("{} keeps running for next action after {}".format(self.name,self.active_action))
    actualtime = datetime.datetime.now()
    actualtimestr = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    action_settings = kwargs["action_settings"]
    for settings in action_settings:
      for entity_name,entity_settings in settings.items():
        if "." in entity_name:
          type, entity_name_part = self.split_entity(entity_name)
          if type == "binary_sensor":
            type = "sensor"
        else:
          type = entity_name
        self.debug_log("{} {}".format(entity_name,entity_settings))
        if self.language["delay"] in entity_settings:
          delay = int(entity_settings[self.language["delay"]])
        else:
          delay = 0
        self.debug_log("delay set to {}".format(delay))  
        sanitize = self.get_app("actions_helpers")
        entity_settings[self.language["value"]] = sanitize.sanitize(entity_settings[self.language["value"]],self.language_name,entity_name)
        self.debug_log("value sanitised to {}".format(entity_settings[self.language["value"]]))  
        action_app = self.get_app("actions_" + type)
        self.run_in(action_app.action, delay, entity = entity_name, entity_settings = entity_settings)
        self.run_in(self.action_log, delay, entity = entity_name, value = entity_settings[self.language["value"]],type = self.language["action"])

  def split_if_statement(self,element,conditions):
    #########################################################################################
    # find out type and entity name
    #########################################################################################
    if not element in self.special_element_types:
      type, entity_name = self.split_entity(element)
    else:
      type = element
      entity_name = element
    #########################################################################################
    # set the delay
    #########################################################################################
    if self.language["delay"] in conditions:     
      time_to_action2 = conditions[self.language["delay"]]
    else:
      time_to_action2 = 0  
    #########################################################################################
    # set the offset
    #########################################################################################
    if "offset" in conditions:
      offset = conditions[self.language["offset"]]
    else:
      offset = 0
    #########################################################################################
    # check if starttime is set
    #########################################################################################
    if self.language["start"] in conditions:
      start_time = self.parse_time(conditions[self.language["start"]])
      start_time_set = True
    else:
      start_time = None
      start_time_set = False
    #########################################################################################
    # check if new state is set
    #########################################################################################
    if self.language["new_state"] in conditions:
      new_state = conditions[self.language["new_state"]]
      use_new_state = True
    else:
      new_state = ""
      use_new_state = False
    #########################################################################################
    # check if old state is set
    #########################################################################################
    if self.language["old_state"] in conditions:
      old_state = conditions[self.language["old_state"]]
      use_old_state = True
    else:
      old_state = ""
      use_old_state = False
    #########################################################################################
    # check if attribute is set
    #########################################################################################
    if self.language["attribute"] in conditions:
      attribute = conditions[self.language["attribute"]]
      use_attribute = True
    else:
      attribute = ""
      use_attribute = False

    return type, entity_name, time_to_action2, offset, start_time, start_time_set, new_state, old_state, attribute, use_new_state, use_old_state, use_attribute

  #########################################################################################
  # the actual constraint part is set in the helpers app
  #########################################################################################
  def custom_constraint(self, conditions):
    constraints = self.get_app("actions_helpers")
    constrain = constraints.custom_constraint(conditions, self.debug_logging, self.language_name)
    return constrain

  #########################################################################################
  # the actual logging is set in the helpers app
  #########################################################################################
  def action_log(self, kwargs):
    entity = kwargs["entity"]
    value = kwargs["value"]
    if entity == "hourly":
      value = "-"
    type = kwargs["type"]
    if not self.action_logging:
      return
    #action_logging = self.get_app("actions_helpers")
    #action_logging.action_log(entity + ";" + str(value) + ";" + str(type))
    fr_entity = entity
    if "." in entity:
      if self.entity_exists(entity):
        fr_entity = self.friendly_name(entity)
    if value == None or type == None:
      self.log("unexpected value {} for {}".format(value,fr_entity))
    self.log("{};{};{}".format(fr_entity,value,type),log = "actions")
    runtime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    try:
      type = type.ljust(9," ")[:9]
      appname = self.name.ljust(40," ")[:40]
      log = open("/mnt/usbdrive/pi/HAlogs/actions/{}.csv".format(entity), 'a')
      log.write("{} ;{} ;{} ;{}\n".format(runtime,type,appname,value))
      log.close()
    except:
      self.log("LOGFILE /mnt/usbdrive/pi/HAlogs/actions/{}.csv NIET BEREIKBAAR".format(entity),level = "WARNING")

  def debug_log(self, message):
    if self.app_config["actions_helpers"]["debug"]:
      try:
        runtime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        log = open("/mnt/usbdrive/pi/HAlogs/actions/debug/{}.log".format(self.name), 'a')
        log.write("{} ;{}\n".format(runtime,message))
        log.close()
      except:
        self.log("LOGFILE /mnt/usbdrive/pi/HAlogs/actions/debug/{}.log NIET BEREIKBAAR".format(self.name),level = "WARNING")

