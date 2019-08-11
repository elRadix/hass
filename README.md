# Hello there! 👋

So this is my Home Assistant instance 🎉

This repository exists mostly for my own amusement, but it may contain some things that others might find useful.

## Statistics from the instance

Description | Value
-- | --
Entities in the [`alert`](https://www.home-assistant.io/components/alert) domain | 6
Entities in the [`automation`](https://www.home-assistant.io/components/automation) domain | 317
Entities in the [`binary_sensor`](https://www.home-assistant.io/components/binary_sensor) domain | 58
Entities in the [`climate`](https://www.home-assistant.io/components/climate) domain | 6
Entities in the [`counter`](https://www.home-assistant.io/components/counter) domain | 10
Entities in the [`device_tracker`](https://www.home-assistant.io/components/device_tracker) domain | 18
Entities in the [`geo_address`](https://www.home-assistant.io/components/geo_address) domain | 5
Entities in the [`group`](https://www.home-assistant.io/components/group) domain | 68
Entities in the [`input_boolean`](https://www.home-assistant.io/components/input_boolean) domain | 45
Entities in the [`input_datetime`](https://www.home-assistant.io/components/input_datetime) domain | 12
Entities in the [`input_number`](https://www.home-assistant.io/components/input_number) domain | 36
Entities in the [`input_select`](https://www.home-assistant.io/components/input_select) domain | 7
Entities in the [`input_text`](https://www.home-assistant.io/components/input_text) domain | 2
Entities in the [`light`](https://www.home-assistant.io/components/light) domain | 40
Entities in the [`lock`](https://www.home-assistant.io/components/lock) domain | 1
Entities in the [`media_player`](https://www.home-assistant.io/components/media_player) domain | 2
Entities in the [`person`](https://www.home-assistant.io/components/person) domain | 2
Entities in the [`script`](https://www.home-assistant.io/components/script) domain | 95
Entities in the [`sensor`](https://www.home-assistant.io/components/sensor) domain | 408
Entities in the [`sun`](https://www.home-assistant.io/components/sun) domain | 1
Entities in the [`switch`](https://www.home-assistant.io/components/switch) domain | 116
Entities in the [`timer`](https://www.home-assistant.io/components/timer) domain | 16
Entities in the [`utility_meter`](https://www.home-assistant.io/components/utility_meter) domain | 4
Entities in the [`weather`](https://www.home-assistant.io/components/weather) domain | 1
Entities in the [`zone`](https://www.home-assistant.io/components/zone) domain | 9

## Hardware and general setup

For my setup I use an old Lenovo Yoga Pro 2, it has a touch screen so I have mounted it on the wall by the front door so I can easily access some controls in my Lovelace UI.

OS | Ubuntu desktop 18.04
-- | --
SSD | 512GB
RAM | 8GB
Processor | Intel® Core™ i7-4500U Processor
Connectivity | WiFi

For the installation method of Home Assistant I went with [the generic Linux installation of Hassio](https://www.home-assistant.io/hassio/installation/#alternative-install-on-a-generic-linux-host)

This method stores the files used by hassio/Home Assistant in `/usr/share/hassio`.

I have mounted a share from my NAS to the `/usr/share/hassio` dir, that way I can handle backups and replication on my NAS.

For my theme I use [slate](https://github.com/seangreen2/slate_theme) on all my devices for two reasons, it looks good and I can track it in HACS.

To access my instance I'm using my [Nabu Casa ❤️](https://www.nabucasa.com/) link.

## Core integrations that I use

- [AdGuard Home](https://www.home-assistant.io/components/adguard/)
- [Belkin WeMo](https://www.home-assistant.io/components/wemo/)
- [Default Config](https://www.home-assistant.io/components/default_config/)
- [Entur public transport](https://www.home-assistant.io/components/entur_public_transport/)
- [File](https://www.home-assistant.io/components/file/)
- [Input Boolean](https://www.home-assistant.io/components/input_boolean/)
- [Met.no](https://www.home-assistant.io/components/met/)
- [Shell command](https://www.home-assistant.io/components/shell_command/)
- [Spotify](https://www.home-assistant.io/components/spotify/)


## custom_components that I use

A summary of custom_components that I use.

### [Raspberry Pi Power Supply Checker](https://github.com/custom-components/sensor.rpi_power/blob/master/README.md)

### [UI Template binary_sensor configuration](https://github.com/dlashua/templatebinarysensor)

### [UI Template sensor configuration](https://github.com/custom-components/templatesensor)

### [HACS (Home Assistant Community Store)](https://custom-components.github.io/hacs)

_Manage (Install, track, upgrade) and discover custom elements for Home Assistant._

I use this to discover new awesome stuff, and to keep the custom elements I use up to date with the latest version of it from the developer.

### [Sun2](https://github.com/pnbruckner/ha-sun2/blob/master/README.md)

### [Composite](https://github.com/pnbruckner/homeassistant-config/blob/master/docs/composite.md)

### [geo_address](https://github.com/Sha-Darim/geo_address)

### [Lovelace Gen]()

### [Sun](https://www.home-assistant.io/components/sun)

### [Illuminance](https://github.com/pnbruckner/homeassistant-config/blob/master/docs/illuminance.md)

### [Ophaalkalender](https://github.com/pippyn/Home-Assistant-Sensor-Ophaalkalender)

### [Shelly smart home](https://github.com/StyraHem/ShellyForHASS/blob/master/README.md)

### [Docker Monitor](https://github.com/Sanderhuisman/docker_monitor)

### [HANotify](https://github.com/Crewski/HANotify)

### [Places](https://github.com/tenly2000/HomeAssistant-Places)

### [BWAlarm (ak74 edition)](https://github.com/akasma74/Hass-Custom-Alarm)

### [Breaking Changes](https://github.com/custom-components/breaking_changes)

### [Generate readme](https://github.com/custom-components/readme)

_Generates this awesome readme file._

I use this integration to generate this readme, and to convert my lovelace configuration.

### [Bravia TV PSK](https://github.com/custom-components/media_player.braviatv_psk)


## Custom Lovelace plugins that I use

A summary of custom Lovelace plugins that I use.

### [Compact Custom Header](https://github.com/maykar/compact-custom-header)

_CCH - Customize the header and add enhancements to Lovelace. Features: kiosk mode, conditional header styling, per user/device views, swiping between views on mobile, and more._

I use this to get more screen space by minifying the space used by the header, and to lock my laptop that I have in the hallway by the door to one view.

### [Favicon Counter](https://github.com/custom-cards/favicon-counter)

_Show a notification count badge.._

I use this to show a badge on the Home Assistant tab in my browser when there are active [Persistent notifications](https://www.home-assistant.io/components/persistent_notification/)

### [Mini Graph Card](https://github.com/kalkih/mini-graph-card)

_Minimalistic graph card for Home Assistant Lovelace UI_

I use this to create beautiful statistics cards for my UI.

***

Like all other Home Assistant instances this is also a Work in Progress :D