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
        hass.services.call('script', 'lights', '', False)
        time.sleep(15)
        state = hass.states.get(ls).state
        lights = (hass.states.get(ls).attributes["friendly_name"])
        time.sleep(1)
        hass.services.call('notify', 'dageraad', {'message': lights + ' are now ' + state })
        logger.info('Easyplus lights off')

  if sw.state == 'on':
        hass.services.call('script', 'switches', '', False)
        time.sleep(15)
        state = hass.states.get(sw).state
        switches = (hass.states.get(sw).attributes["friendly_name"])
        time.sleep(1)
        hass.services.call('notify', 'dageraad', {'message': switches + ' are now ' + state })
        logger.info('Easyplus Switches off')

  hass.services.call('switch', 'turn_off', { 'entity_id': 'switch.easyplus' }, False)
  time.sleep(5)
  state = hass.states.get(ep).state
  switch = (hass.states.get(ep).attributes["friendly_name"])
  time.sleep(1)
  hass.services.call('notify', 'dageraad', {'message': switch + ' is now ' + state })
  logger.info('Easyplus Switches off')

doWork(hass, data, logger)
