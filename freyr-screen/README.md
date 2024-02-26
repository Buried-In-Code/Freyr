# Freyr - Screen

![Micropython](https://img.shields.io/badge/Micropython-1.22.2-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Beta-yellowgreen?style=flat-square)

_TODO_

## Components

- [Raspberry Pi Pico W](https://www.raspberrypi.com/products/raspberry-pi-pico/)
- [Waveshare 2.9 ePaper Module](https://core-electronics.com.au/waveshare-2-9inch-e-paper-module-for-raspberry-pi-pico-296x128-black-white.html)

## Installation

1. Download and load the [Micropython uf2](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) onto your Pico.
2. Install [mpremote](https://pypi.org/project/mpremote/).
3. Install external dependencies:
   - `mpremote mip install urequests`
4. Copy the config file to your device: `mpremote cp config.py :`
5. Update the `config.py` file with your settings: `mpremote edit config.py`
6. Copy the display file to your device: `mpremote cp waveshare_display.py :`
7. Copy the main file to your device: `mpremote cp main.py :`
