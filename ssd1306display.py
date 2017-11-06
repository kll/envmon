from ssd1306 import SSD1306_I2C

from sensordata import SensorData

class Ssd1306Display:

    def __init__(self, width, height, address, i2c):
        self.Display = SSD1306_I2C(width, height, i2c, address)

    def show(self, data, wl):
        self.Display.fill(0)
        self.Display.text(str.format("T: {:.1f}F", data.Temperature), 0, 0)
        self.Display.text(str.format("H: {:.1f}%", data.Humidity), 0, 10)
        self.Display.text(str.format("P: {:.1f}hPa", data.Pressure), 0, 20)
        self.Display.text(str.format("SSID: {}", wl.ssid()), 0, 54)
        self.Display.show()

