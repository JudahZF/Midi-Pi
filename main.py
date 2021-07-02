from machine import Pin, UART, I2C
import ustruct, gc, utime
from time import sleep, sleep_ms, sleep_us
from lcd_driver import I2cLcd
from midi import *

# Blink LED to confirm Sucessful Boot
activeLED = Pin(25, Pin.OUT)
bootCheck = 0
while bootCheck < 4:
    activeLED.toggle()
    sleep_ms(100)
    activeLED.toggle()
    sleep_ms(100)
    bootCheck+=1

# LCD Setup
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
print("Hex address: ",hex(I2C_ADDR))
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.blink_cursor_off()
lcd.clear()
lcd.hide_cursor()

# Midi Setup
midiOUT = UART(0,31250)
midiIN = UART(1,31250)

# Footswitch Pin Exaple
"""
FS0 = Pin(3, Pin.IN, Pin.PULL_DOWN)

x = 0
y = 0
lcd.clear()
lcd.putstr(str(x))
FS0Last = 0
while True:
    print("Pin State", FS0.value(), "Loop", y)
    if (FS0Last != FS0.value()) & (FS0.value() == 0):
        x += 1
        lcd.clear()
        lcd.putstr(str(x))
    FS0Last = FS0.value()
    sleep_ms(25)
    y+=1
"""