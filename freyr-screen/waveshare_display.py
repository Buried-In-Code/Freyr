# *****************************************************************************
# * | File        :      Pico_ePaper-2.9.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-03-16
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

import framebuf
import utime
from machine import SPI, Pin

# Display resolution
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 296

RESET_PIN = 12
DC_PIN = 8
CS_PIN = 9
BUSY_PIN = 13

PARTIAL_LUT = [
    0x0,
    0x40,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x80,
    0x80,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x40,
    0x40,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x80,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0A,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x1,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x22,
    0x22,
    0x22,
    0x22,
    0x22,
    0x22,
    0x0,
    0x0,
    0x0,
    0x22,
    0x17,
    0x41,
    0xB0,
    0x32,
    0x36,
]

FULL_LUT = [
    0x80,
    0x66,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x40,
    0x0,
    0x0,
    0x0,
    0x10,
    0x66,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x20,
    0x0,
    0x0,
    0x0,
    0x80,
    0x66,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x40,
    0x0,
    0x0,
    0x0,
    0x10,
    0x66,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x20,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x14,
    0x8,
    0x0,
    0x0,
    0x0,
    0x0,
    0x2,
    0xA,
    0xA,
    0x0,
    0xA,
    0xA,
    0x0,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x14,
    0x8,
    0x0,
    0x1,
    0x0,
    0x0,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x1,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x0,
    0x44,
    0x44,
    0x44,
    0x44,
    0x44,
    0x44,
    0x0,
    0x0,
    0x0,
    0x22,
    0x17,
    0x41,
    0x0,
    0x32,
    0x36,
]


def digital_write(pin: Pin, value: int) -> None:
    pin.value(value)


def digital_read(pin: Pin) -> int:
    return pin.value()


def delay_ms(delay: int) -> None:
    utime.sleep(delay / 1000.0)


class LandscapeDisplay(framebuf.FrameBuffer):
    def __init__(self) -> None:
        self.reset_pin = Pin(RESET_PIN, Pin.OUT)

        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = DISPLAY_WIDTH
        self.height = DISPLAY_HEIGHT

        self.partial_lut = PARTIAL_LUT
        self.full_lut = FULL_LUT

        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.buffer = bytearray(self.height * self.width // 8)
        super().__init__(self.buffer, self.height, self.width, framebuf.MONO_VLSB)
        self.init()

    def spi_write_byte(self, data) -> None:
        self.spi.write(bytearray(data))

    def module_exit(self) -> None:
        digital_write(pin=self.reset_pin, value=0)

    # Hardware reset
    def reset(self) -> None:
        digital_write(pin=self.reset_pin, value=1)
        delay_ms(delay=50)
        digital_write(pin=self.reset_pin, value=0)
        delay_ms(delay=2)
        digital_write(pin=self.reset_pin, value=1)
        delay_ms(delay=50)

    def send_command(self, command) -> None:
        digital_write(pin=self.dc_pin, value=0)
        digital_write(pin=self.cs_pin, value=0)
        self.spi_write_byte(data=[command])
        digital_write(self.cs_pin, 1)

    def send_data(self, data) -> None:
        digital_write(pin=self.dc_pin, value=1)
        digital_write(pin=self.cs_pin, value=0)
        self.spi_write_byte(data=[data])
        digital_write(pin=self.cs_pin, value=1)

    def send_data1(self, buf) -> None:
        digital_write(pin=self.dc_pin, value=1)
        digital_write(pin=self.cs_pin, value=0)
        self.spi.write(bytearray(buf))
        digital_write(pin=self.cs_pin, value=1)

    def read_busy(self) -> None:
        while digital_read(pin=self.busy_pin) == 1:  # 0: idle, 1: busy
            delay_ms(10)

    def turn_on_display(self) -> None:
        self.send_command(command=0x22)  # DISPLAY_UPDATE_CONTROL_2
        self.send_data(data=0xC7)
        self.send_command(command=0x20)  # MASTER_ACTIVATION
        self.read_busy()

    def turn_on_display_partial(self) -> None:
        self.send_command(command=0x22)  # DISPLAY_UPDATE_CONTROL_2
        self.send_data(data=0x0F)
        self.send_command(command=0x20)  # MASTER_ACTIVATION
        self.read_busy()

    def lut(self, lut) -> None:
        self.send_command(command=0x32)
        self.send_data1(buf=lut[0:153])
        self.read_busy()

    def set_lut(self, lut) -> None:
        self.lut(lut)
        self.send_command(command=0x3F)
        self.send_data(data=lut[153])
        self.send_command(command=0x03)  # gate voltage
        self.send_data(data=lut[154])
        self.send_command(command=0x04)  # source voltage
        self.send_data(data=lut[155])  # VSH
        self.send_data(data=lut[156])  # VSH2
        self.send_data(data=lut[157])  # VSL
        self.send_command(command=0x2C)  # VCOM
        self.send_data(data=lut[158])

    def set_window(self, x_start: int, y_start: int, x_end: int, y_end: int) -> None:
        self.send_command(command=0x44)  # SET_RAM_X_ADDRESS_START_END_POSITION
        # x point must be the multiple of 8 or the last 3 bits will be ignored
        self.send_data(data=(x_start >> 3) & 0xFF)
        self.send_data(data=(x_end >> 3) & 0xFF)
        self.send_command(command=0x45)  # SET_RAM_Y_ADDRESS_START_END_POSITION
        self.send_data(data=y_start & 0xFF)
        self.send_data(data=(y_start >> 8) & 0xFF)
        self.send_data(data=y_end & 0xFF)
        self.send_data(data=(y_end >> 8) & 0xFF)

    def set_cursor(self, x: int, y: int) -> None:
        self.send_command(command=0x4E)  # SET_RAM_X_ADDRESS_COUNTER
        self.send_data(data=x & 0xFF)

        self.send_command(command=0x4F)  # SET_RAM_Y_ADDRESS_COUNTER
        self.send_data(data=y & 0xFF)
        self.send_data(data=(y >> 8) & 0xFF)
        self.read_busy()

    def init(self) -> int:
        # EPD hardware init start
        self.reset()

        self.read_busy()
        self.send_command(command=0x12)  # SWRESET
        self.read_busy()

        self.send_command(command=0x01)  # Driver output control
        self.send_data(data=0x27)
        self.send_data(data=0x01)
        self.send_data(data=0x00)

        self.send_command(command=0x11)  # data entry mode
        self.send_data(data=0x07)

        self.set_window(x_start=0, y_start=0, x_end=self.width - 1, y_end=self.height - 1)

        self.send_command(command=0x21)  # Display update control
        self.send_data(data=0x00)
        self.send_data(data=0x80)

        self.set_cursor(x=0, y=0)
        self.read_busy()

        self.set_lut(lut=self.full_lut)
        # EPD hardware init end
        return 0

    def display(self, image) -> None:
        if image is None:
            return
        self.send_command(command=0x24)  # WRITE_RAM
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(self.height):
                self.send_data(data=image[i + j * self.height])
        self.turn_on_display()

    def display_base(self, image) -> None:
        if image is None:
            return
        self.send_command(command=0x24)  # WRITE_RAM
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(self.height):
                self.send_data(data=image[i + j * self.height])

        self.send_command(command=0x26)  # WRITE_RAM
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(self.height):
                self.send_data(data=image[i + j * self.height])

        self.turn_on_display()

    def display_partial(self, image) -> None:
        if image is None:
            return

        digital_write(pin=self.reset_pin, value=0)
        delay_ms(delay=2)
        digital_write(pin=self.reset_pin, value=1)
        delay_ms(delay=2)

        self.set_lut(lut=self.partial_lut)
        self.send_command(command=0x37)
        self.send_data(data=0x00)
        self.send_data(data=0x00)
        self.send_data(data=0x00)
        self.send_data(data=0x00)
        self.send_data(data=0x00)
        self.send_data(data=0x40)
        self.send_data(data=0x00)
        self.send_data(data=0x00)
        self.send_data(data=0x00)
        self.send_data(data=0x00)

        self.send_command(command=0x3C)  # BorderWaveform
        self.send_data(data=0x80)

        self.send_command(command=0x22)
        self.send_data(data=0xC0)
        self.send_command(command=0x20)
        self.read_busy()

        self.set_window(x_start=0, y_start=0, x_end=self.width - 1, y_end=self.height - 1)
        self.set_cursor(x=0, y=0)

        self.send_command(command=0x24)  # WRITE_RAM
        for j in range(int(self.width / 8) - 1, -1, -1):
            for i in range(self.height):
                self.send_data(data=image[i + j * self.height])
        self.turn_on_display_partial()

    def clear(self, colour) -> None:
        self.send_command(command=0x24)  # WRITE_RAM
        self.send_data1(buf=[colour] * self.height * int(self.width / 8))
        self.send_command(command=0x26)  # WRITE_RAM
        self.send_data1(buf=[colour] * self.height * int(self.width / 8))
        self.turn_on_display()

    def sleep(self) -> None:
        self.send_command(command=0x10)  # DEEP_SLEEP_MODE
        self.send_data(data=0x01)

        delay_ms(delay=2000)
        self.module_exit()


if __name__ == "__main__":
    # Landscape
    epd = LandscapeDisplay()
    epd.clear(colour=0xFF)

    epd.fill(0xFF)
    epd.text("Waveshare", 5, 10, 0x00)
    epd.text("Pico_ePaper-2.9", 5, 20, 0x00)
    epd.text("Raspberry Pico", 5, 30, 0x00)
    epd.display(image=epd.buffer)
    delay_ms(delay=2000)

    epd.vline(10, 40, 60, 0x00)
    epd.vline(120, 40, 60, 0x00)
    epd.hline(10, 40, 110, 0x00)
    epd.hline(10, 100, 110, 0x00)
    epd.line(10, 40, 120, 100, 0x00)
    epd.line(120, 40, 10, 100, 0x00)
    epd.display(image=epd.buffer)
    delay_ms(delay=2000)

    epd.rect(150, 5, 50, 55, 0x00)
    epd.fill_rect(150, 65, 50, 115, 0x00)
    epd.display_base(image=epd.buffer)
    delay_ms(delay=2000)

    for i in range(10):
        epd.fill_rect(220, 60, 10, 10, 0xFF)
        epd.text(str(i), 222, 62, 0x00)
        epd.display_partial(image=epd.buffer)

    epd.init()
    epd.clear(colour=0xFF)
    delay_ms(delay=2000)
    epd.sleep()
