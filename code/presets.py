import midi
import time

class Song ():

    def __init__(self, name, shortName, ssName, bpm, key, PC):
        self.name = name
        self.shortName = shortName
        self.sshortName = ssName
        self.bpm = bpm
        self.key = key
        self.bpmS = 60 / self.bpm
        self.PC = PC
