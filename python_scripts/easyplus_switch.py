def doWork(hass, data, logger):
  sn = data.get('entity_id')
  ep = hass.states.get('switch.easyplus')

  if sn is None:
    logger.warning('<easyplus> no switch id supplied')
    return

  if ep is None:
    logger.warning('<easyplus> switch.easyplus does not exist')
    return

  ss = hass.states.get(sn)

  if ss is None:
    logger.warning('<easyplus> switch does not exist')
    return

  if ep.state == 'off':
    service_data = {'entity_id':'switch.easyplus'}
    hass.services.call('switch', 'turn_on', service_data, False)
    time.sleep(17)

  hass.services.call('switch', 'turn_on', service_data={ 'entity_id': sn })
  hass.services.call('notify', 'dageraad',
                    {'message':'Switch status is {}'.format(ss)})
  hass.services.call('notify', 'dageraad', {'message': ss })


doWork(hass, data, logger)
