# main.py -- put your code here!
import machine
import os
import bme280
import ssd1306
import time

#from deepsleep import DeepSleep
import deepsleep
from sensordata import SensorData

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
DISPLAY_ADDRESS = 0x3c
PIN_I2C_SDA = 'P9'
PIN_I2C_SCL = 'P8' # deault is P10 but that conflicts with deepsleep shield
PIN_WAKE = 'P17'

def main():
    """The main loop of the program."""
    ds = deepsleep.DeepSleep()
    ds.enable_pullups(PIN_WAKE)
    ds.enable_wake_on_fall(PIN_WAKE)
    
    wl, bme, oled = init()
    
    temperature, pressure, humidity = bme.read_compensated_data()
    data = SensorData()
    data.Temperature = round((temperature / 100) * 1.8 + 32, 1)
    data.Humidity = round(humidity / 1024, 1)
    data.Pressure = round(pressure / 256 / 100, 1)
        
    # get the wake reason and the value of the pins during wake up
    wake_s = ds.get_wake_status()
    if wake_s['wake'] == deepsleep.PIN_WAKE:
        print("Pin wake up")
        oled.fill(0)
        oled.text(str.format("T: {:.1f}F", data.Temperature), 0, 0)
        oled.text(str.format("H: {:.1f}%", data.Humidity), 0, 10)
        oled.text(str.format("P: {:.1f}hPa", data.Pressure), 0, 20)
        oled.text(str.format("SSID: {}", wl.ssid()), 0, 54)
        oled.show()
        time.sleep(5)
    elif wake_s['wake'] == deepsleep.TIMER_WAKE:
        print("Timer wake up")
        # report sensor data remotely
    else:  # deepsleep.POWER_ON_WAKE:
        print("Power ON reset")
        oled.fill(0)
        oled.text(str.format("T: {:.1f}F", data.Temperature), 0, 0)
        oled.text(str.format("H: {:.1f}%", data.Humidity), 0, 10)
        oled.text(str.format("P: {:.1f}hPa", data.Pressure), 0, 20)
        oled.text(str.format("SSID: {}", wl.ssid()), 0, 54)
        oled.show()
        # wait for a while in case we need to update software
        time.sleep(60)
    
    ds.go_to_sleep(60)
        
def init():
    """Initialize required IO objects."""
    from network import WLAN
    wl = WLAN()
    i2c = machine.I2C(0, pins=(PIN_I2C_SDA, PIN_I2C_SCL))
    #i2c.init(machine.I2C.MASTER, baudrate=100000)
    bme = bme280.BME280(i2c=i2c)
    oled = ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c, DISPLAY_ADDRESS)
    return wl, bme, oled

if __name__ == '__main__':
    main()
