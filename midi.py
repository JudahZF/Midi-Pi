from machine import Pin, UART, I2C
import ustruct, gc, utime
from time import sleep, sleep_ms, sleep_us

# Defines diffent possible midi messages
class midi ():
    def __init__ (MidiOut, MidiIn, ActiveLED, self):
        self.LED = ActiveLED
        self.IN = MidiIn
        self.OUT = MidiOut
    def sendNote(note, self):
        self.LED.value(1)
        self.OUT.write(ustruct.pack("bbb",0x90,note,127))
        sleep(50)
        self.LED.value(0)
        sleep(50)
        self.OUT.write(ustruct.pack("bbb",0x80,note,0))

    def sendCC(program, value, self):
        self.LED.value(1)
        sleep_ms(50)
        self.OUT.write(b"\xb0" + program.to_bytes(1, "big") + value.to_bytes(1, "big"))
        sleep_ms(50)
        self.LED.value(0)

    def sendPC(program, self):
        self.OUT.write(b"\xc0" + program.to_bytes(1, "big"))

    def read(self):
        return self.IN.read()

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