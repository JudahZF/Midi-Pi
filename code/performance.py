import midi, time, ui, midi, sys
import effects as FX
from log import log

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
            if i == 0 or (4 <= i and i <= 6) or i == 10 or (14 <= i and i <= 16):
                actions.append(liveAction((self.ccstart+i), 127, False, 1))
            else: actions.append(liveAction((self.ccstart+i), 127, False, 0))
            log(str("Added CC: " + str(i+self.ccstart)))

        self.lcd.print("#")

        # Import Footswitches
        for i in range(10):
            self.FootSwitches[i].setAction(
                actions[i], actions[i+10]
            )
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
            FSin = FX.checkFS(self.FootSwitches, 0.5)
            if FSin[0] is True:
                log(str(FSin[1] + " Pressed"))