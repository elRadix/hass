def doWork(hass, data, logger):
  lights = 'script.lights'
  switches = 'script.switches'
  main = 'switch.easyplus'
  time  = hass.states.get('sensor.time').state

  ep = hass.states.get('switch.easyplus')
  ls = hass.states.get('group.easyplus_lights')
  sw = hass.states.get('group.easyplus_switches')
# time  = hass.states.get('sensor.time').state
# header  = ( 'Easysplus') + ' @ ' + time

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
        hass.services.call('switch', 'turn_on', service_data, False)
        time.sleep(15)
        hass.services.call('notify', 'dageraad', {'message': 'Lights off'})
        logger.info('Easyplus lights off')

  if sw.state == 'on':
        service_data = {'entity_id':'script.switches'}
        hass.services.call('switch', 'turn_on', service_data, False)
        time.sleep(15)
        hass.services.call('notify', 'dageraad', {'message': 'Switches off'})
        logger.info('Easyplus switches off')

  hass.services.call('switch', 'turn_off', service_data={ 'entity_id': main })
  hass.services.call('notify', 'dageraad', {'message': 'Easyplus off'})
  logger.info('Easyplus off')

doWork(hass, data, logger)
