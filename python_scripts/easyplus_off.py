def doWork(hass, data, logger):
  ep = hass.states.get('switch.easyplus')
  ls = hass.states.get('group.easyplus_lights')
  sw = hass.states.get('group.easyplus_switches')

  if ep is None:
    logger.warning('<easyplus> switch.easyplus does not exist')
    return

  if ls is None:
    logger.warning('<easyplus> group lights does not exist')
    return
  if sw is None:
    logger.warning('<easyplus> group switches does not exist')
    return

  if ls.state == 'on':
        service_data = {'entity_id':'script.lights'}
        hass.services.call('script', 'turn_on', service_data, False)
        time.sleep(15)
        hass.services.call('notify', 'dageraad', {'message': 'Lights off'})
        logger.info('Easyplus lights off')

  if sw.state == 'on':
        service_data = {'entity_id':'script.switches'}
        hass.services.call('script', 'turn_on', service_data, False)
        time.sleep(15)
        hass.services.call('notify', 'dageraad', {'message': 'Switches off'})
        logger.info('Easyplus switches off')

  service_data = {'entity_id':'switch.easyplus'}
  hass.services.call('switch', 'turn_off', service_data, False)
  hass.services.call('notify', 'dageraad', {'message': 'Easyplus off'})
  logger.info('Easyplus off')

doWork(hass, data, logger)
