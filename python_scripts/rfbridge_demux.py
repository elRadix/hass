d = { '0DF00A':['inkomhal','ON','true'],
      '0DF00E':['inkomhal','OFF','true'],
      '0DF006':['inkomhal-battery','ON','true'],
      '12800A':['terras','ON','true'],
      '12800E':['terras','OFF','true'],
      '128006':['terras-battery','ON','true'],
      'AC25E8':['fire','ON','true'],
      'AC25E8off':['fire','OFF','true'],
      'DC7503':['gas','ON','true'],
      'DC7503off':['gas','OFF','true'],
      '2C8B11':['water-keuken','ON','true'],
      '2C8B11off':['water-keuken','OFF','true'],
      '628A11':['water-badkamer','ON','true'],
      '628A11off':['water-badkamer','OFF','true'],
      '909601':['circle1','ON','false']
     }


p = data.get('payload')

if p is not None:
  if p in d.keys():
    service_data = {'topic':'home/{}'.format(d[p][0]), 'payload':'{}'.format(d[p][1]), 'qos':0, 'retain':'{}'.format(d[p][2])}
  else:
    service_data = {'topic':'home/unknown', 'payload':'{}'.format(p), 'qos':0, 'retain':'false'}
    logger.warning('<rfbridge_demux> Received unknown RF command: {}'.format(p))
  hass.services.call('mqtt', 'publish', service_data, False)

# if p is not None:
#   if p in d.keys():
#     service_data = {'topic':'home/{}'.format(d[p][0]), 'payload':'{}'.format(d[p][1]), 'qos':0, 'retain':'{}'.format(d[p][2])}
#     hass.services.call('mqtt', 'publish', service_data, False)
#   else:
#     logger.warning('<rfbridge_demux> Received unknown RF command: {}'.format(p))
#     service_data = {'message':'{} - {}'.format(datetime.datetime.now().strftime("%d %b, %X"), p)}
#     hass.services.call('notify', 'log_unknown_rf_codes', service_data, False)
