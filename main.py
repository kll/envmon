# main.py -- put your code here!
import machine
import os
import bme280
import ssd1306
import time

from sensordata import SensorData

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
DISPLAY_ADDRESS = 0x3c

def main():
    """The main loop of the program."""
    wl, bme, oled = init()

    while True:
        temperature, pressure, humidity = bme.read_compensated_data()
        data = SensorData()
        data.Temperature = round((temperature / 100) * 1.8 + 32, 1)
        data.Humidity = round(humidity / 1024, 1)
        data.Pressure = round(pressure / 256 / 100, 1)
        
        oled.fill(0)
        oled.text(str.format("T: {:.1f}F", data.Temperature), 0, 0)
        oled.text(str.format("H: {:.1f}%", data.Humidity), 0, 10)
        oled.text(str.format("P: {:.1f}hPa", data.Pressure), 0, 20)
        oled.text(str.format("SSID: {}", wl.ssid()), 0, 54)
        oled.show()

        time.sleep(1)

def init():
    """Initialize required IO objects."""
    from network import WLAN
    wl = WLAN()
    i2c = machine.I2C()
    bme = bme280.BME280(i2c=i2c)
    oled = ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c, DISPLAY_ADDRESS)
    return wl, bme, oled


if __name__ == '__main__':
    main()
