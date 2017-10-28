# main.py -- put your code here!
import machine
import bme280

i2c = machine.I2C()
bme = bme280.BME280(i2c=i2c)

print(bme.values)
