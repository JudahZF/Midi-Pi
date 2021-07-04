from machine import *
import ustruct, gc, utime, midi
from time import *

class effect ():
    
    def __init__(self, name, type, program, value = 0, state = False):
        self.name = name
        self.type = type
        self.program = program
        self.value = value
        self.state = state
        if type == 0:
            self.write = midi.momentaryNote(self.program)
        elif type == 1:
            self.write = midi.sendCC(self.program, self.value)
        elif type == 2:
            self.write = midi.sendPC(self.program, self.value)
            
    def write(self):
        self.write()
        self.state.toggle()
    
    def setState(self, state):
        if state != self.state:
            self.write()
            self.state.toggle()

class footSwitch ():
    
    def __init__(self, number, pin):
        self.no = number
        self.IO = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        
    def setEffect(self, effect, holdEffect, upEffect, rightEffect, state):
        self.effect = effect
        self.holdEffect = holdEffect
        self.upEffect = upEffect
        self.rightEffect = rightEffect
    
    def setMode(self, mode):
        if mode == 0:
            self.action = self.effect
            self.upAction = self.upEffect
            self.holdAction = self.holdEffect
            self.rightAction = self.rightEffect
        elif mode == 1:
            break
            
    def up(self):
        self.upAction()
    
    def right(self):
        self.rightAction()
    
    def tap(self):
        self.action()
    
    def hold(self):
        self.holdAction()


# FS setup
x = 0
def checkFS(FS, time):
    for i in FS:
        if (x == 4) or (x == 8):
            if FS[x].IO.value() == 1:
                start_time = time()
                while FS[x].IO.value() == 1: pass
                holdTime = start_time - time()
                if holdTime >= 3: FS[x].hold()
                else: FS[x].tap()
        elif x == 0:
            if FS[x].IO.value() == 1:
                start_time = time()
                while FS[x].IO.value() == 1: pass
                holdTime = start_time - time()
                if holdTime >= 3:
                    if (FS[x].IO.value() == 1) & (FS[x-2].IO.value() == 1): FS[x].up()
                    else: FS[x].hold()
                else: FS[x].tap()
        elif (x == 5) or (x == 9):
            if FS[x].IO.value() == 1:
                start_time = time()
                while FS[x].IO.value() == 1: pass
                holdTime = start_time - time()
                if holdTime >= 3:
                    if (FS[x].IO.value() == 1) & (FS[x+1].IO.value() == 1): FS[x].right()
                    else: FS[x].hold()
                else: FS[x].tap()
        else:
            if FS[x].IO.value() == 1:
                start_time = time()
                while FS[x].IO.value() == 1: pass
                holdTime = start_time - time()
                if holdTime >= 3:
                    if (FS[x].IO.value() == 1) & (FS[x-2].IO.value() == 1): FS[x].up()
                    elif (FS[x].IO.value() == 1) & (FS[x+1].IO.value() == 1): FS[x].right()
                    else: FS[x].hold()
                else: FS[x].tap()
        x=x+1