# main.py -- put your code here!
import machine
import bme280
import ssd1306

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64

def main():
    """The main loop of the program."""
    bme, oled = init()

    while True:
        print(bme.values)
        
        oled.fill(0)
        oled.text(bme.values, 0, 0)
        oled.show()

def init():
    """Initialize required IO objects."""
    i2c = machine.I2C()
    bme = bme280.BME280(i2c=i2c)
    oled = ssd1306.SSD1306_I2C(DISPLAY_WIDTH, DISPLAY_HEIGHT, i2c)
    return oled, bme


if __name__ == '__main__':
    main()
