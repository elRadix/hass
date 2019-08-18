sn = data.get('entity_main')
sub = data.get('entity_sub')
ep = hass.states.get('switch.easyplus')

if sn is not None:
  ss = hass.states.get(sn)
  if ss is not None:
    if ep is not None:
      if ep.state == 'off':
        service_data = {'entity_id':'switch.easyplus'}
        hass.services.call('switch', 'turn_on', service_data, False)
        hass.services.call('notify', 'dageraad', {'message':  'Starting EasyPlus' })
        time.sleep(20)

      hass.services.call('switch', 'toggle', service_data={ 'entity_id': sn })
      time.sleep(2)
      state = hass.states.get(sn).state
      switch = (hass.states.get(sn).attributes["friendly_name"])
      time.sleep(1)
      hass.services.call('notify', 'dageraad', {'message': switch + ' is now ' + state })

      hass.services.call('switch', 'toggle', service_data={ 'entity_id': sub })
      time.sleep(2)
      state = hass.states.get(sub).state
      switch = (hass.states.get(sub).attributes["friendly_name"])
      time.sleep(1)
      hass.services.call('notify', 'dageraad', {'message': switch + ' is now ' + state })

    else:
      logger.warning('<easyplus> switch.easyplus does not exist')
  else:
    logger.warning('<easyplus> switch does not exist')
else:
  logger.warning('<easyplus> no switch supplied')
