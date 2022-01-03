import midi, time, ui, midi, sys
import effects as FX
from log import log

class Song ():

    def __init__(self, name, shortName, ssName, bpm, key, PC):
        self.name = name
        self.shortName = shortName
        self.sshortName = ssName
        self.bpm = bpm
        self.key = key
        self.bpmS = 60 / self.bpm
        self.PC = PC

class mode ():
    def __init__(self, lcd, presetFile, fs, midi):
        self.mode = "Preset"
        self.presetFile = presetFile
        self.lcd = lcd
        self.FootSwitches = fs
        self.midiHost = midi

    def run (self):
        if self.presetFile == "":
            self.lcd.clear()
            self.lcd.print("Add a preset file")
            time.sleep(30)
            self.lcd.clear()
            sys.exit()
        songs = []
        actions = []
        set = self.presetFile["Set Name"]
        # Save All Songs to Songs Array
        for i in self.presetFile["songs"]:
            songs.append(
                Song(i["name"], i["sName"], i["ssName"], i["bpm"], i["key"], i["PC"])
            )
            log(str("Adding Song: " + i["name"]))
        self.lcd.print("#")

        # Import Effects to Actions Array
        for i in self.presetFile["actions"]:
            actions.append(FX.action(i["name"], i["type"], i["program"], i["value"], False))
            log(str("Action Action: " + i["name"]))

        self.lcd.print("#")

        # Import Footswitches
        x = 0
        for i in self.presetFile["FSAction"]:
            self.FootSwitches[x].setAction(
                actions[i["action"]], actions[i["holdAction"]]
            )
            x = x + 1
        log(str("Set Up Footswitches"))
        self.lcd.print("#")

        self.lcd.set_cursor_pos(3, 10)
        self.lcd.print("Done!     ")

        currentSongNo = self.presetFile["currentSong"]
        songNo = currentSongNo

        # GUI Reprint Function
        def PrintGui (l3Mode, FSLine):
            self.lcd.print(ui.line0(set, "Preset"))
            self.lcd.print(ui.line1(songs[int(songNo)], "Both"))
            self.lcd.print(ui.line2(self.midiHost, "Preset"))
            self.lcd.print(ui.line3(self.mode, l3Mode, FSLine))

        # Print First GUI
        PrintGui("clear", "Nothing Here")
        log(str("Main UI Printed"))

        # Main Loop
        timePress = 0
        timeSincePress = 0
        cleared = True
        while True:
            # Check for New Song
            songNo = midi.checkSong(currentSongNo, "Preset")
            if songNo is not currentSongNo:
                try:
                    self.lcd.home()
                    PrintGui("clear", (FSin[1]))
                    currentSongNo = songNo
                except Exception as e:
                    log(str("Change Song Error: " + str(e)))

            # Check For Footswitch Press
            FSin = FX.checkFS(self.FootSwitches, 0.5)
            if FSin[0] is False:
                timeSincePress = time.monotonic() - timePress
                if (timeSincePress >= 5) and (cleared == False):
                    PrintGui("clear", "Nerds")
                    log(str("Cleared GUI"))
                    cleared = True
                pass
            elif FSin[0] is True:
                timePress = time.monotonic()
                log(str("FS " + FSin[1] + " Pressed"))
                timeSincePress = 0
                self.lcd.home()
                cleared = False
                PrintGui("loop", (FSin[1]))