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
        time.sleep(17)

      hass.services.call('switch', 'toggle', service_data={ 'entity_id': sn })
      hass.services.call('switch', 'toggle', service_data={ 'entity_id': sub })

    else:
      logger.warning('<easyplus> switch.easyplus does not exist')
  else:
    logger.warning('<easyplus> switch does not exist')
else:
  logger.warning('<easyplus> no switch supplied')