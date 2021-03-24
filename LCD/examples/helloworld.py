import i2c_lcd
from machine import I2C

i2c = I2C(1,sda=sda, scl=scl, freq=400000)
d = i2c_lcd.Display(i2c)

d.home()
d.write('Hello World')
