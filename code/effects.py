import midi
import time
import digitalio

class action:
    def __init__(self, name, type, program, value, state):
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
            midi.sendPC(self.program)
        elif self.type == 3:
            midi.sendPC(self.program)
        elif self.type == 9:
            print(self.program)

    def toggle(self):
        self.write()
        self.state = not self.state

    def setState(self, state):
        if state != self.state:
            self.write()
            self.toggle()


class footSwitch:
    def __init__(self, number, pin):
        self.no = number
        self.IO = digitalio.DigitalInOut(pin)
        self.action = action("fsnull0", 9, 127)
        self.holdAction = action("fsnull1", 9, 0)

    def setAction(self, action, holdAction):
        self.action = action
        self.holdAction = holdAction

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
            while i.IO.value() is True:
                pass
            holdTime = start_time - time()
            if holdTime >= Htime:
                i.hold()
            else:
                i.tap()
            tapped = True
    return tapped
