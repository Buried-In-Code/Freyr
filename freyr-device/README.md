# Freyr - Device

![Micropython](https://img.shields.io/badge/Micropython-1.20.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

Collects temperature and humidity readings and sends them to Freyr.

## Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [DHT22 sensor](https://core-electronics.com.au/dht22-module-temperature-and-humidity.html)

## Installation

1. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
2. Install [mpremote](https://pypi.org/project/mpremote/).
3. Install external dependencies:
   - `mpremote mip install dht`
   - `mpremote mip install urequests`
4. Copy the config file to your device: `mpremote cp config.py :`
5. Update the `config.py` file with your settings: `mpremote edit config.py`
6. Copy the main file to your device: `mpremote cp main.py :`
