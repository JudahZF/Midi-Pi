from machine import *
import ustruct, gc, utime, midi
from time import *

class action ():
    
    def __init__(self, name, type, program, value = 0, state = False):
        self.name = name
        self.type = type
        self.program = program
        self.value = value
        self.state = state
    
    def write(self):
        if self.type == 0:
            midi.momentaryNote(self.program)
        elif self.type == 1:
            midi.sendCC(self.program, self.value)
        elif self.type == 2:
            midi.sendPC(self.program, self.value)
        elif self.type == 9:
            print(self.program)
            
    def toggle(self):
        self.write()
        self.state = not self.state
    
    def setState(self, state):
        if state != self.state:
            self.write()
            self.toggle()

class footSwitch ():
    
    def __init__(self, number, pin):
        self.no = number
        self.IO = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.action = action("fsnull0", 9, 127)
        self.holdAction = action("fsnull1", 9, 0)
    
    def setAction(self, mode, action, holdAction):
        if mode == 0:
            self.action = action
            self.holdAction = holdAction
        elif mode == 1:
            print("MODE ERROR")
            
    def tap(self):
        self.action.toggle()
    
    def hold(self):
        self.holdAction.toggle()


# FS setup

def checkFS(FS, Htime):
    tapped = False
    for i in FS:
        if i.IO.value() == 1:
            start_time = time()
            while i.IO.value() == 1: pass
            holdTime = start_time - time()
            if holdTime >= Htime: i.hold()
            else: i.tap()
            tapped = True
    if tapped == False: return False
    elif tapped == True: return True