from machine import Pin, UART, I2C
import time, ustruct, liquidcrystal_i2c
#Show blink LED to confirm Sucessful Boot
activeLED = Pin(25, Pin.OUT)
bootCheck = 0
while bootCheck < 2:
    activeLED.toggle()
    time.sleep_ms(500)
    bootCheck+=1

midiOUT = UART(0,31250)
midiIN = UART(1,31250)
#Footswitch Var template Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

#Defines diffent possible midi messages
def sendMidiNote(note):
    activeLED.value(1)
    midiOUT.write(ustruct.pack("bbb",0x90,note,127))
    time.sleep(0.5)
    activeLED.value(0)
    time.sleep(0.5)
    midiOUT.write(ustruct.pack("bbb",0x80,note,0))

def sendMidiCC(program, value):
    activeLED.value(1)
    time.sleep(0.5)
    midiOUT.write(b"\xb0" + program.to_bytes(1, "big") + value.to_bytes(1, "big"))
    time.sleep(0.5)
    activeLED.value(0)

def sendMidiPC(program):
    midiOUT.write(b"\xc0" + program.to_bytes(1, "big"))

def midiRead():
    return midiIN.read()

class footswitch():
    def __init__ (self):
        self.value = 0
        self.program = 0
        self.type = 0 #Types cc = 0 pc = 1 notes = 2
    
    def setup (self, type, program):
        if str(type).lower() == "cc":
            self.type = 0
        elif str(type).lower() == "pc":
            self.type = 1
        elif str(type).lower() == "notes":
            self.type = 2
        else: self.type = 0
        self.program = program
    
    def sendMessage (self):
        if self.type == 0:
            sendMidiCC(self.program, self.value)
        elif self.type == 1:
            sendMidiPC(self.program)
        elif self.type == 2:
            sendMidiNote(self.value)

sda=Pin(20)
scl=Pin(21)
i2c=I2C(0,sda=sda, scl=scl, freq=400000)
print(i2c.scan())
i2c.writeto(39, '\x04')
i2c.writeto(39, '\x01')
i2c.writeto(39, '\x02')
#i2c.writeto(39, "hello world")
"""
cols = 20
rows = 4

lcd = liquidcrystal_i2c.LiquidCrystal_I2C(0x27, 1, numlines=rows)

lcd.printline(0, 'LCM2004 IIC V2'.center(cols))
lcd.printline(1, 'and'.center(cols))
lcd.printline(2, 'python-')
lcd.printline(3, 'liquidcrystal_i2c'.rjust(cols))"""