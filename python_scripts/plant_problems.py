# Creates the following sensors:
#
# sensor.plants_water_number      -> Amount of plants that need to be watered
# sensor.plants_water_friendly    -> Name(s) of the plants that need water
# sensor.plants_battery_number    -> Amount of plantsensors running out of battery
# sensor.plants_battery_friendly  -> Name(s) of platsensors running out of battery
# sensor.plants_problems          -> Amount of plants which either need water or have low battery
#
#  INSPIRED BY THIS GREAT BLOGPOST
#  http://www.diyfuturism.com/making-houseplants-talk

problemPlants = 0
allproblemPlants = []
waterPlants = []
numberWater = 0
deadBatteries = []
numberdeadBatteries = 0
whichIcon = "mdi:help-circle-outline"

for entity_id in hass.states.entity_ids('plant'):
    state = hass.states.get(entity_id)
    if state.state == 'problem':
        problemPlants = problemPlants + 1
        allproblemPlants.append(state.name)
        problem = state.attributes.get('problem') or 'none'
        if "moisture low" in problem:
          waterPlants.append(state.name)
          numberWater = numberWater + 1
        if "battery low" in problem:
          deadBatteries.append(state.name)
          numberdeadBatteries = numberdeadBatteries + 1

# Set icon
if problemPlants > 0:
  whichIcon = "mdi:alert-circle-outline"
else:
  whichIcon = "mdi:check-circle-outline"

# Set states
hass.states.set('sensor.plants_problems', problemPlants, {
    'unit_of_measurement': 'Plants',
    'friendly_name': 'Problem plants',
    'icon': whichIcon,
    'problem_plants': allproblemPlants,
    'water': waterPlants,
    'water_number': numberWater,
    'battery_change': deadBatteries,
    'battery_number': numberdeadBatteries
})

hass.states.set('sensor.plants_water_number', numberWater, {
    'unit_of_measurement': 'Plants',
    'friendly_name': 'Num. thirsty plants',
    'icon': 'mdi:water'
})

hass.states.set('sensor.plants_battery_number', numberdeadBatteries, {
    'unit_of_measurement': 'Sensors',
    'friendly_name': 'Num. battery-powered sensors',
    'icon': 'mdi:battery-30'
})

waterplantsList = ', '.join(waterPlants)
if waterplantsList == "":
  waterplantsList = "Keine"
hass.states.set('sensor.plants_water_friendly', waterplantsList, {
    'friendly_name': 'Thirsty plants',
    'icon': 'mdi:water'
})

batteryplantsList = ', '.join(deadBatteries)
if batteryplantsList == "":
  batteryplantsList = "None"
hass.states.set('sensor.plants_battery_friendly', batteryplantsList, {
    'friendly_name': 'Low battery sensors',
    'icon': 'mdi:battery-30'
})