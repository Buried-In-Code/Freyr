# Freyr - Device

![Micropython](https://img.shields.io/badge/Micropython-1.20.0-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

Collects temperature and humidity readings and sends them to Freyr.

## Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [DHT22 sensor](https://core-electronics.com.au/dht22-module-temperature-and-humidity.html)

## Installation

1. Update the `config.py` file with your settings
2. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
3. Install [mpremote](https://pypi.org/project/mpremote/).
4. Install external dependencies:
   - `mpremote mip install dht`
   - `mpremote mip install urequests`
5. Copy the config file to your device: `mpremote cp config.py :`
6. Copy the main file to your device: `mpremote cp main.py :`
