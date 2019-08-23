if 'entity_id' not in data:
    logger.warning("===== entity_id is required if you want to set something.")
else:
    data = data.copy()
    inputEntity = data.pop('entity_id')
    inputStateObject = hass.states.get(inputEntity)
    if inputStateObject:
        inputState = inputStateObject.state
        inputAttributesObject = inputStateObject.attributes.copy()
    else:
        inputState = 'unknown'
        inputAttributesObject = {}
    if 'state' in data:
        inputState = data.pop('state')
    logger.debug("===== new attrs: {}".format(data))
    inputAttributesObject.update(data)

    hass.states.set(inputEntity, inputState, inputAttributesObject)