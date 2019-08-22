def doWork(hass, data, logger):
  sn = data.get('switch_id')
  ep = hass.states.get('switch.easyplus')
  ss = hass.states.get(sn)
  switch = (hass.states.get(sn).attributes["friendly_name"])

  if sn is None:
    logger.warning('<easyplus_switch> no switch id supplied')
    return

  if ep is None:
    logger.warning('<easyplus_switch> switch.easyplus does not exist')
    return

  if ss is None:
    logger.warning('<easyplus_switch> switch does not exist')
    return

  if ep.state == 'off':
    service_data = {'entity_id':'switch.easyplus'}
    hass.services.call('switch', 'turn_on', service_data, False)
    time.sleep(20)

  hass.services.call('switch', 'toggle', service_data={ 'entity_id': sn })
  time.sleep(4)
  hass.services.call('notify', 'dageraad', {'message': switch + ': ' + ss.state})

doWork(hass, data, logger)
