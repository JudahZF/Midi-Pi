import midi, time, ui, midi, sys
import effects as FX
from log import log

class mode ():
    def __init__(self, lcd, liveFile, fs, midi):
        self.mode = "Live"
        self.liveFile = liveFile
        self.lcd = lcd
        self.FootSwitches = fs
        self.midiHost = midi

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
        for i in self.liveFile["actions"]:
            actions.append(FX.action(i["name"], i["type"], i["program"], i["value"], False))
            log(str("Action Action: " + i["name"]))

        self.lcd.print("#")

        # Import Footswitches
        x = 0
        for i in self.liveFile["FSAction"]:
            self.FootSwitches[x].setAction(
                actions[i["action"]], actions[i["holdAction"]]
            )
            x = x + 1
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
        PrintGui("test", "C", 140, "Intro", "Verse", "Clear", "")
        log(str("Main UI Printed"))

        # Main Loop
        timePress = 0
        timeSincePress = 0
        cleared = True
        currentSong = []
        while True:
            # Check for New Song
            songInfo = midi.checkSong(currentSong, "Live")
            #songInfo = midi.partChange(songInfo)
            if songInfo is not currentSong:
                try:
                    PrintGui(songInfo[0], songInfo[1], songInfo[2], songInfo[3], songInfo[4], FSin[1], "")
                    currentSong = songInfo
                except Exception as e:
                    log(str("Change Song Error: " + str(e)))

            # Check For Footswitch Press
            FSin = FX.checkFS(self.FootSwitches, 0.5)
            if FSin[0] is False:
                timeSincePress = time.monotonic() - timePress
                if (timeSincePress >= 5) and (cleared == False):
                    PrintGui("clear", "Nerds", self.mode)
                    log(str("Cleared GUI"))
                    cleared = True
                pass
            elif FSin[0] is True:
                timePress = time.monotonic()
                log(str("FS " + FSin[1] + " Pressed"))
                timeSincePress = 0
                cleared = False
                PrintGui("loop", (FSin[1]), self.mode)