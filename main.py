from machine import *
import ustruct, gc, utime, json
from time import *
from lcd_driver import I2cLcd
from effects import *
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
i2c = I2C(0, sda=Pin(2), scl=Pin(3), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.blink_cursor_off()
lcd.clear()
lcd.hide_cursor()
lcd.backlight_on()

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

# Boot Screen
#           --------------------
lcd.putstr("      Midi  Pi      ")
lcd.putstr(" Please set effects ")
lcd.putstr(" to default values  ")
lcd.putstr(" Booting:")

# Define Footswitches 6-15
FootSwitches = [footSwitch(0, 6), footSwitch(1, 7), footSwitch(2, 8), footSwitch(3, 9), footSwitch(4, 10), footSwitch(5, 11), footSwitch(6, 12), footSwitch(7, 13), footSwitch(8, 14), footSwitch(9, 15)]
lcd.putchar("#")

# Load JSON
file = open("settings.json", 'r')
settings = json.load(file)
file.close()
lcd.putchar("#")
print(settings)
if str(settings) == "{}":
    print("empty JSON")
if settings["firstSetup"] == True:
    

# Main Loop
"""
While True:

"""

sleep(4)
lcd.backlight_off()
print("off")
lcd.clear()