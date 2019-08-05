sn = data.get('switch_id')
ep = hass.states.get('switch.easyplus')

if sn is not None:
  ss = hass.states.get('script.' + sn)
  if ss is not None:
    if ep is not None:
      if ep.state == 'off':
        service_data = {'entity_id':'switch.easyplus'}
        hass.services.call('switch', 'turn_on', service_data, False)
        time.sleep(20)

        hass.services.call('switch', 'turn_on', service_data={ 'entity_id': 'sn' })
    else:
      logger.warning('<easyplus> switch.easyplus does not exist.')
  else:
    logger.warning('<easyplus> Supplied script does not exist.')
else:
  logger.warning('<easyplus> No script name was supplied.')