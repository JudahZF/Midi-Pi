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
        if (self.doToggle):
            if (self.state):
                midi.sendCC(self.program, self.value)
            else:
                midi.sendCC(self.program, 0)
            print("Sent CC:" + str(self.program))
            self.state = not self.state
        else:
            midi.sendCC(self.program, self.value)
            print("Sent CC:" + str(self.program))
            self.state = not self.state
        

    def setState(self, state):
        if state != self.state:
            self.write()
            self.toggle()


class mode ():
    def __init__(self, lcd, liveFile, fs, midi, CC):
        self.mode = "Live"
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
            if i == 0 or (4 <= i and i <= 6):
                actions.append(liveAction((self.ccstart+i), 127, False, True))
            else: actions.append(liveAction((self.ccstart+i), 127, False, False))
            log(str("Added CC: " + str(i+self.ccstart)))
        
        actions[0] = liveAction((self.ccstart+i), 127, False, False)
        actions[4] = liveAction((self.ccstart+i), 127, False, False)
        actions[5] = liveAction((self.ccstart+i), 127, False, False)
        actions[6] = liveAction((self.ccstart+i), 127, False, False)

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
        def PrintGui (name, key, BPM, currPart, nxtPart, l3Mode, FSLine):
            self.lcd.home()
            self.lcd.print(ui.line0(name, "Live"))
            self.lcd.print(ui.line1(key+":"+str(BPM), "Live"))
            self.lcd.print(ui.line2(currPart+":"+nxtPart, "Live"))
            self.lcd.print(ui.line3(self.mode, l3Mode, FSLine))

        # Print First GUI
        PrintGui("", "", 120, "", "", "Clear", "")
        log(str("Main UI Printed"))

        # Main Loop
        timePress = 0
        timeSincePress = 0
        cleared = True
        currentSong = ["", "", 120, "", ""]
        songInfo = ["", "", 120, "", ""]
        l3 = "Clear"
        while True:
            # Check for New Song
            songInfo = midi.checkSong(currentSong, "Live")
            FSin = FX.checkFS(self.FootSwitches, 0.5)
            if songInfo is not currentSong:
                try:
                    PrintGui(songInfo[0], songInfo[1], songInfo[2], songInfo[3], songInfo[4], l3, FSin[1])
                    currentSong = songInfo
                except Exception as e:
                    log(str("Change Song Error: " + str(e)))

            # Check For Footswitch Press
            if FSin[0] is False:
                timeSincePress = time.monotonic() - timePress
                if (timeSincePress >= 1) and (cleared == False):
                    l3 = "Clear"
                    PrintGui(songInfo[0], songInfo[1], songInfo[2], songInfo[3], songInfo[4], l3, FSin[1])
                    log(str("Cleared GUI"))
                    cleared = True
                pass
            elif FSin[0] is True:
                timePress = time.monotonic()
                log(str(FSin[1] + " Pressed"))
                timeSincePress = 0
                cleared = False
                l3 = "loop"
                PrintGui(songInfo[0], songInfo[1], songInfo[2], songInfo[3], songInfo[4], l3, FSin[1])