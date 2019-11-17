#
# this app contains helper functions for the actions app
# included are:
# - sanitize
# - custom_constraints
# - action_log
#

import appdaemon.plugins.hass.hassapi as hass
import random
import datetime

class actions_helpers(hass.Hass):

    def initialize(self):
        return

    ################################################################################
    # this next function sanitizes the value from the actions.
    # an action value can contain 
    # an entity value like {{platform.entity_name}}
    # an attribute value like {{platform.entity_name.attribute_name}}
    # a value up like {{+5}} (this will add 5 to the entity value)
    # a value down like {{-3}} (this will deduct 3 from the entity value)
    # a time like {{time}} (this will set the entity state to the actual time)
    # 
    # example action:
    # sensor.something_last_updated: {"value": "{{time}}"}
    # or
    # sensor.people_in_house:
    #   value: "{{-1}}"
    ################################################################################
    def sanitize(self,value,language,entity=""):
        #########################################################################################
        # lets start by seeing if we need to translate:
        #########################################################################################
        self.language = self.app_config["actions_language_" + language]
        #value = self.cleanup(value)

        if "{{" in str(value) and "}}" in str(value):
            if "+" in value and entity != "":
                value = value[2:-2]
                value = str(int(self.get_state(entity)) + int(value[1:]))
            elif "-" in value and "." in entity:
                value = value[2:-2]
                value = str(int(self.get_state(entity)) - int(value[1:]))
            elif self.language["time"] in value:
                value = datetime.datetime.now().strftime("%H:%M:%S")
            else:
                parts = value.split("{{") 
                valuepart1 = parts[0]
                lastparts = parts[1].split("}}")
                valuepart2 = lastparts[1]
                newvalue = lastparts[0]
                if "[" in newvalue:
                    valuelist = newvalue[1:-1].split(",")
                    rndvalue = random.choice(valuelist)
                    value = valuepart1 + rndvalue + valuepart2
                else:
                    sensorparts = newvalue.split(".")
                    if len(sensorparts) == 3:
                        myattribute = True
                        attributevalue = sensorparts[2]
                        sensor = sensorparts[0] + "." + sensorparts[1]
                    else:
                        sensor = newvalue
                        myattribute = False
                    if myattribute:
                        sensorvalue = str(self.get_state(sensor, attribute = attributevalue))
                    else:
                        sensorvalue = str(self.get_state(sensor))
                        sensorvalue = sensorvalue.replace(".",",")
                    value = valuepart1 + sensorvalue + valuepart2
        return value

    def cleanup(self, value):
        if not isinstance(value, str):
            return value
        unwanted_characters = ["-","/","\\","<",">"]
        for character in unwanted_characters:
            value = value.replace(character,"")
        return value

    ################################################################################
    # this next function checks if the action needs to take place.
    # a constraint can contain:
    # an entity and its value 
    # an entity and a list of values
    # a list of weekdays
    # a start and entime (or a sensor containing a time)
    # 
    # examples:
    # hold_for:
    #   sensor.something: 25
    #   switch.something: "on"
    #   time: {"start": "12:00:00", "end": "14:00:00"}
    #   time: {"start": "sensor.bed_time_start", "end": "06:00:00"}
    #   weekday: [1,2,3,4,5]  (from 1 to 7)
    #   sensor.something: ["home","away","at work"]
    ################################################################################
    def custom_constraint(self, conditions, debug_logging, language):
        #########################################################################################
        # lets start by seeing if we need to translate:
        #########################################################################################
        #debug_logging = True
        if "no_hold" in conditions:
            if debug_logging:
                self.log("no hold for was set")
            return True
        self.language = self.app_config["actions_language_" + language]
        #self.log("hold conditions are: {}".format(conditions))
        for condition in conditions:
            for device,value in condition.items():
                #if debug_logging:
                #    self.log("hold for: {} value: {}".format(device,value))
                if device == self.language["weekday"]:
                    for _day in value:
                        if (datetime.datetime.today().weekday() + 1) == _day:
                            if debug_logging:
                                self.log("i will hold for: {} value: {}".format(device, _day))
                            return False
                elif device == self.language["time"]:
                    if "sensor" in value[self.language["start"]]:
                        starttime = self.get_state(value[self.language["start"]])
                    else:
                        starttime = value[self.language["start"]]
                    if "sensor" in value[self.language["end"]]:
                        endtime = self.get_state(value[self.language["end"]])
                    else:
                        endtime = value[self.language["end"]]
                    if self.now_is_between(starttime,endtime):
                        if debug_logging:
                            self.log("i will hold for: {}".format(device))
                        return False
                elif isinstance(value, list):
                    for eachvalue in value:
                        if str(self.get_state(device)) == str(eachvalue):
                            if debug_logging:
                                self.log("i will hold for: {} value: {}".format(device,eachvalue))
                            return False
                elif str(self.get_state(device)) == str(value):
                    if debug_logging:
                        self.log("i will hold for: {} value: {}".format(device,value))
                    return False
                if debug_logging:
                    self.log("didnt hold for: " + device)
        return True


    ################################################################################
    # this next function takes care of the action logging so we can have a 
    # seperate overview.
    ################################################################################
    def action_log(self, message):
        #self.log(message,log = "actions")
        return
