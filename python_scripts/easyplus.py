def doWork(hass, data):
  sn = data.get('script_id')
  ep = hass.states.get('switch.easyplus')

  if sn is None:
    logger.warning('<easyplus> No script id was supplied.')
    return

  if ep is None:
    logger.warning('<easyplus> switch.easyplus does not exist.')
    return

  ss = hass.states.get('script.' + sn)

  if ss is None:
    logger.warning('<easyplus> Supplied script does not exist.')
    return

  if ep.state == 'off':
    service_data = {'entity_id':'switch.easyplus'}
    hass.services.call('switch', 'turn_on', service_data, False)
    ep = hass.states.get('switch.easyplus')

  wait_until = ep.last_changed + datetime.timedelta(seconds=17)
  while wait_until > datetime.now():
      time.sleep(1)

  hass.services.call('script', sn, '', False)


doWork(hass, data)