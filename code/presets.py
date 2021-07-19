import ustruct, gc, utime, midi, effects
from time import *

class Song ():
    
    def __init__ (self, name, shortName, ssName, bpm, key, PC):
        self.name = name
        self.shortName = shortName
        self.sshortName = ssName
        self.bpm = bpm
        self.key = key
        self.bpmS = 60 / self.bpm
        self.PC = PC
    
    def sendPC(self):
        midi.sendPC(self.PC)
    
    def sendBPM (self, midiBPM):
        sleep_ms(10)
        midiBPM()
        sleep(self.bpmS)
        midiBPM()
        sleep(self.bpmS)
        midiBPM()
        sleep(self.bpmS)
        midiBPM()
        sleep_ms(10)