import midi
import time
import digitalio

class action:
    def __init__(self, name, typeNo, program, value, state):
        self.name = name
        self.type = typeNo
        self.program = program
        self.value = value
        self.state = state

    # Toogle The Footswitch
    def toggle(self):
        if self.type == 0:
            midi.sendCC(self.program, self.value)
            print("Sent CC:" + str(self.program))
        elif self.type == 1:
            midi.sendPC(self.program)
        elif self.type == 9:
            pass # System Response
        self.state = not self.state

    def setState(self, state):
        if state != self.state:
            self.write()
            self.toggle()


class footSwitch:
    def __init__(self, number, pin):
        self.no = number
        self.io = digitalio.DigitalInOut(pin)
        self.io.direction = digitalio.Direction.INPUT
        self.io.pull = digitalio.Pull.DOWN
        self.IO = self.io
        self.tapAction = action("fsnull0", 9, 127, 0, False)
        self.holdAction = action("fsnull1", 9, 0, 0, False)
        self.tapAction = self.tapAction
        self.holdAction = self.holdAction

    # Set The actions of the Footswitch
    def setAction(self, action, holdAction):
        self.tapAction = action
        self.holdAction = holdAction

    def tap(self):
        try:
            self.tapAction.toggle()
            print("Tap")
        except  Exception as E:
            print(str(E))

    def hold(self):
        try:
            self.holdAction.toggle()
            print("Hold")
        except  Exception:
            print("ERROR")

# FS setup

def checkFS(FS, LastState):
    tapped = False
    x = 0
    held = ""
    no = 0
    for i in FS:
        # Check For pressed Footswitch
        if (i.IO.value is not LastState[i]) and (i.IO.value is True):
            no = x
            i.tap()
            held = ("FS " + str(x) + " Tapped")
            tapped = True
            LastState[i] = not LastState[i]
        else: x = x + 1
    return [tapped, held, no, LastState]

def checkFS(FS, LastState, Htime):
    tapped = False
    x = 0
    held = ""
    no = 0
    for i in FS:
        # Check For pressed Footswitch
        if i.IO.value is True:
            no = x
            # Save Start Time
            start_time = time.monotonic()
            while i.IO.value is True:
                # Wait
                pass
            # Save End Time
            holdTime = time.monotonic() - start_time
            # Decide whether to hold or tap footswitch
            if holdTime >= Htime:
                i.hold()
                held = ("FS " + str(x) + " Held")
            else:
                i.tap()
                held = ("FS " + str(x) + " Tapped")
            tapped = True
        else: x = x + 1
    return [tapped, held, no]
