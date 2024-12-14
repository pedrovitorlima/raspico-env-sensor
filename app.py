import time
import board
import busio
import adafruit_ltr390

i2c = busio.I2C(scl=board.GP21, sda=board.GP20)
ltr = adafruit_ltr390.LTR390(i2c)

while True:
    print("UV:", ltr.uvs, "\t\tAmbient Light:", ltr.light)
    print("UVI:", ltr.uvi, "\t\tLux:", ltr.lux)
    time.sleep(1.0)
