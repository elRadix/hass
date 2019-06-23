class TrashCard extends HTMLElement {
  set hass(hass) {
    if (!this.content) {
      const card = document.createElement('ha-card');
      const link = document.createElement('link');
      link.type = 'text/css';
      link.rel = 'stylesheet';
      link.href = '/local/custom_ui/trash_card/trash-card.css';
      card.appendChild(link);
      this.content = document.createElement('div');
      this.content.className = 'card';
      card.appendChild(this.content);
      this.appendChild(card);
      
      card.header = 'Afvalwijzer'
    }

    var states = this.config.entities.map(x => hass.states[x]);
    var nextPickupInDaysSensor = hass.states['sensor.trash_next'];
    var stateObjects = states.sort(function(x,y){
      var xValue = x.state.split('-').reverse().join('');
      var yValue = y.state.split('-').reverse().join('');
      if (xValue < yValue)
        return -1;
      if (xValue > yValue)
        return 1;
      return 0;
    }).map(function(x){
      var date = new Date(x.state.split('-').reverse().join('-'));
     
      var stateObject = {
        HassState: x,
        Date: date
      };
      return stateObject;
    });
    this.content.innerHTML = `
      <span>
        <ul class="variations right">
            <li></li>
        </ul>
        <ul class="variations">
        <li><span class="ha-icon"><ha-icon icon="mdi:numeric-${nextPickupInDaysSensor.state}-box-multiple-outline"></ha-icon></span>&nbsp;dagen tot volgende afhaaldag.</li>
            <li></li>
        </ul>
      </span>
      <div class="forecast clear">
          ${stateObjects.map(function(stateObject){ 
            var state =stateObject.HassState;
            var today = new Date();
            var isToday = today.toDateString() === stateObject.Date.toDateString();
            return ` <div class="day">
                  <span class="dayname2">${state.attributes.friendly_name}</span>
                  <br><i class="icon" style="background: none, url(${state.attributes.entity_picture}) no-repeat; background-size: contain;"></i>
                  <br><span class="highTemp">${isToday?"vandaag": state.state}</span>
              </div>`
              }).join('')}
      </div>`;
  }

  setConfig(config) {
    if (!config.entities) {
      throw new Error('Please provide entities');
    }
    this.config = config;
  }

  // @TODO: This requires more intelligent logic
  getCardSize() {
    return 3;
  }
}

customElements.define('trash-card', TrashCard);