from machine import *
import ustruct, gc, utime
from time import *

activeLED = Pin(25, Pin.OUT)
midiOUT = UART(0,31250)
midiIN = UART(1,31250)

def noteOn(note):
    midiOUT.write(ustruct.pack("bbb",0x90,note,127))
    
def noteOff(note):
    midiOUT.write(ustruct.pack("bbb",0x80,note,0))
    
def momentaryNote(note):
    noteOn(note)
    sleep_ms(50)
    noteOff(note)

def sendCC(program, value):
    sleep_ms(50)
    midiOUT.write(b"\xb0" + program.to_bytes(1, "big") + value.to_bytes(1, "big"))
    sleep_ms(50)

def sendPC(program):
    midiOUT.write(b"\xc0" + program.to_bytes(1, "big"))

def read():
    return midiIN.read()
