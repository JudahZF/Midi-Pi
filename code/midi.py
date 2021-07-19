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

# Footswitch Class
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

fstest = Pin(2, Pin.IN, Pin.PULL_DOWN)