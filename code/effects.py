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
            
    def toggle(self):
        self.write
        self.state = not self.state
    
    def setState(self, state):
        if state != self.state:
            self.write()
            self.state.toggle()

class footSwitch ():
    
    def __init__(self, number, pin):
        self.no = number
        self.IO = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.effect = False
        self.holdEffect = False
        self.upEffect = False
        self.rightEffect = False
        
    def setEffect(self, effect, holdEffect, upEffect, rightEffect):
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
            print("MODE ERROR")
            
    def up(self):
        self.upAction()
    
    def right(self):
        self.rightAction()
    
    def tap(self):
        self.action()
    
    def hold(self):
        self.holdAction()


# FS setup

def checkFS(FS, Htime):
    tapped = False
    x = 0
    for i in FS:
        if (x == 4) or (x == 8):
            if i.IO.value() == 1:
                start_time = time()
                while i.IO.value() == 1: pass
                holdTime = start_time - time()
                if holdTime >= Htime: i.hold()
                else: i.tap()
                tapped = True
        elif x == 0:
            if i.IO.value() == 1:
                start_time = time()
                while i.IO.value() == 1: pass
                holdTime = start_time - time()
                if holdTime >= Htime:
                    if (i.IO.value() == 1) & (FS[x-2].IO.value() == 1): i.up()
                    else: i.hold()
                else: i.tap()
                tapped = True
        elif (x == 5) or (x == 9):
            if i.IO.value() == 1:
                start_time = time()
                while i.IO.value() == 1: pass
                holdTime = start_time - time()
                if holdTime >= Htime:
                    if (i.IO.value() == 1) & (FS[x+1].IO.value() == 1): i.right()
                    else: i.hold()
                else: i.tap()
                tapped = True
        elif (x == 1) or (x == 2) or (x == 3) or (x == 6) or (x == 7):
            if i.IO.value() == 1:
                start_time = time()
                while i.IO.value() == 1: pass
                holdTime = start_time - time()
                if holdTime >= Htime:
                    if (i.IO.value() == 1) & (FS[x-2].IO.value() == 1): i.up()
                    elif (i.IO.value() == 1) & (FS[x+1].IO.value() == 1): i.right()
                    else: i.hold()
                else: i.tap()
                tapped = True
        x=x+1
    if tapped == False: return False
    elif tapped == True: return True