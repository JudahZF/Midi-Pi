from machine import *
import time, ustruct, ujson
#Show blink LED to confirm Sucessful Boot
activeLED = Pin(25, Pin.OUT)
bootCheck = 0
while bootCheck < 8:
    activeLED.toggle()
    time.sleep_ms(500)
    bootCheck+=1

midiOUT = UART(1,31250)
#Footswitch Var template Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN)

def sendMidi(note):
    activeLED.value(1)
    midiOUT.write(ustruct.pack("bbb",0x90,note,127))
    time.sleep(0.5)
    activeLED.value(0)
    time.sleep(0.5)
    midiOUT.write(ustruct.pack("bbb",0x80,note,0))