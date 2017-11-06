# main.py -- put your code here!
import machine
import os
import bme280
import ssd1306
import time
import deepsleep

from machine import Pin
from sensordata import SensorData
from ssd1306display import Ssd1306Display

PIN_I2C_SDA = 'P9'
PIN_I2C_SCL = 'P8' # deault is P10 but that conflicts with deepsleep shield
PIN_WAKE = 'P17'
PIN_DEV = 'P18'

def main():
    """The main loop of the program."""
    ds = deepsleep.DeepSleep()
    ds.enable_pullups([PIN_WAKE, PIN_DEV])
    ds.enable_wake_on_fall([PIN_WAKE, PIN_DEV])

    wl, bme, display = init()
    
    temperature, pressure, humidity = bme.read_compensated_data()
    data = SensorData()
    data.Temperature = round((temperature / 100) * 1.8 + 32, 1)
    data.Humidity = round(humidity / 1024, 1)
    data.Pressure = round(pressure / 256 / 100, 1)

    # get the wake reason and the value of the pins during wake up
    wake_s = ds.get_wake_status()
    if wake_s['wake'] == deepsleep.PIN_WAKE:
        print("Pin wake up")
        display.show(data, wl)
        time.sleep(5)
    elif wake_s['wake'] == deepsleep.TIMER_WAKE:
        print("Timer wake up")
        # report sensor data remotely
    else:  # deepsleep.POWER_ON_WAKE:
        print("Power ON reset")
        display.show(data, wl)
    
    dev_pin = Pin(PIN_DEV, mode=Pin.IN)
    if dev_pin() == 0:  # don't sleep if dev pin is held low so that remote connections to update code can be made
        print("Not sleeping due to dev mode.")
    else:
        ds.go_to_sleep(60)
        
def init():
    """Initialize required IO objects."""
    from network import WLAN
    wl = WLAN()
    i2c = machine.I2C(0, pins=(PIN_I2C_SDA, PIN_I2C_SCL))
    #i2c.init(machine.I2C.MASTER, baudrate=100000)
    bme = bme280.BME280(i2c=i2c)
    display = Ssd1306Display(128, 64, 0x3c, i2c)
    return wl, bme, display

if __name__ == '__main__':
    main()
