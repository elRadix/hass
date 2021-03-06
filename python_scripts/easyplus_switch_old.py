
###
def doWork(hass, data, logger):
  sn = data.get('entity_id')
  ep = hass.states.get('switch.easyplus')
  ss = hass.states.get(sn)
  id = (hass.states.get(sn).attributes["friendly_name"])


  if sn is None:
     logger.warning('<easyplus> no switch id supplied')
     return

  if ep is None:
     logger.warning('<easyplus> switch.easyplus does not exist')
     retur

  if ss is None:
     logger.warning('<easyplus> switch does not exist')
     return

  hass.services.call('notify', 'dageraad', {'message':' Toggle ' + id })

  if ep.state == 'off':
     service_data = {'entity_id':'switch.easyplus'}
     hass.services.call('switch', 'turn_on', service_data, False)
     hass.services.call('notify', 'dageraad', {'message':  'Starting EasyPlus' })
     time.sleep(22)
     hass.services.call('notify', 'dageraad', {'message':  'Startup EasyPlus completed' })
     #time.sleep(5)


  hass.services.call('switch', 'toggle', service_data={ 'entity_id': sn })
 # time.sleep(3)
 # state = hass.states.get(sn).state
 # switch = (hass.states.get(sn).attributes["friendly_name"])
 # time.sleep(2)
 # hass.services.call('notify', 'dageraad', {'message': switch + ' is now ' + state })

doWork(hass, data, logger)

# switch_group = 'group.easyplus_switches'

# entities_on = []
# for entity_id in hass.states.get(switch_group).attributes['entity_id']:
#     if hass.states.get(entity_id).state is 'on':
#         entities_on.append(hass.states.get(entity_id).attributes["friendly_name"])

# if len(entities_on) > 0:
#     notification_message = "The following Switches are on: " + ', '.join(entities_on)
#     hass.services.call('notify', 'dageraad', {'message': notification_message})
