def doWork(hass, data, logger):
  sn = data.get('script_id')
  ep = hass.states.get('switch.easyplus')

  if sn is None:
    logger.warning('<easyplus> no script id supplied')
    return

  if ep is None:
    logger.warning('<easyplus> switch.easyplus does not exist')
    return

  ss = hass.states.get('script.' + sn)

  if ss is None:
    logger.warning('<easyplus> script does not exist')
    return

  if ep.state == 'off':
    service_data = {'entity_id':'switch.easyplus'}
    hass.services.call('switch', 'turn_on', service_data, False)
    hass.services.call('notify', 'dageraad', {'message':  'Starting EasyPlus' })
    time.sleep(20)

  hass.services.call('script', sn, '', False)

doWork(hass, data, logger)
