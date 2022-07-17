import midi, time, ui, midi, sys
import effects as FX
from log import log
import sys
import countio
import digitalio
import board
import pwmio

class liveAction:
    def __init__(self, program, value, state, doToggle):
        self.program = program
        self.doToggle = doToggle
        self.value = value
        self.state = state

    # Toogle The Footswitch
    def toggle(self):
        if (self.doToggle == 1):
            if (self.state == 1):
                midi.sendCC(self.program, self.value)
                print("Sent CC:" + str(self.program) + " Value: "+ str(self.value))
                self.state = 0
            else:
                midi.sendCC(self.program, 0)
                print("Sent CC:" + str(self.program) + " Value: "+ str(0))
                self.state = 1
        else:
            midi.sendCC(self.program, self.value)
            print("Sent CC:" + str(self.program) + " Value: "+ str(self.value))
        
        

    def setState(self, state):
        if state != self.state:
            self.write()
            self.toggle()


class mode ():
    def __init__(self, lcd, liveFile, fs, midi, CC):
        self.mode = "Perf"
        self.liveFile = liveFile
        self.lcd = lcd
        self.FootSwitches = fs
        self.midiHost = midi
        self.ccstart = CC

    def run (self):
        if self.liveFile == "":
            self.lcd.clear()
            self.lcd.print("Add a live file")
            time.sleep(30)
            self.lcd.clear()
            sys.exit()
        actions = []
        self.lcd.print("#")

        # Import Effects to Actions Array
        for i in range(20):
            actions.append(liveAction((self.ccstart+i), 127, False, 0))
            log(str("Added CC: " + str(i+self.ccstart)))

        self.lcd.print("#")

        # Import Footswitches
        timeSince = []
        pinCountArray = []
        for i in range(len(self.FootSwitches)):
            self.FootSwitches[i].setAction(
                actions[i], actions[i+10]
            )
            self.FootSwitches[i].setDIOMode(False)
            pinCountArray.append(countio.Counter(self.FootSwitches[i].pin, edge=countio.Edge.RISE, pull=digitalio.Pull.DOWN))
            timeSince.append(time.monotonic())
        log(str("Set Up Footswitches"))
        self.lcd.print("#")

        self.lcd.set_cursor_pos(3, 10)
        self.lcd.print("Done!     ")

        # GUI Reprint Function
        def PrintGui (l3Mode, FSLine):
            self.lcd.home()
            self.lcd.print(ui.line0("", "Perf"))
            self.lcd.print(ui.line1("", "Perf"))
            self.lcd.print(ui.line2("", "Perf"))
            self.lcd.print(ui.line3(self.mode, l3Mode, FSLine))

        # Print First GUI
        PrintGui("Clear", "")
        log(str("Main UI Printed"))
        
        
        while True:
            # Check for New Song
            # FSin = FX.checkFSNoHold(self.FootSwitches, LastState)
            for i in range(0, len(self.FootSwitches)):
                if pinCountArray[i].count >= 1:
                    now = time.monotonic()
                    pinCountArray[i].reset()
                    if (timeSince[i] < (now-0.15)):
                        self.FootSwitches[i].tap()
                        timeSince[i] = now
                        log(str("FS " + str(i) + " Tapped"))