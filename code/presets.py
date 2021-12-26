import midi, time, ui, midi
import effects as FX
from log import log
from settings import presetFile, settingsFile
from main import FootSwitches, mode, midiHost, lcd

class Song ():

    def __init__(self, name, shortName, ssName, bpm, key, PC):
        self.name = name
        self.shortName = shortName
        self.sshortName = ssName
        self.bpm = bpm
        self.key = key
        self.bpmS = 60 / self.bpm
        self.PC = PC

def run ():
    songs = []
    actions = []
    set = presetFile["Set Name"]
    # Save All Songs to Songs Array
    for i in presetFile["songs"]:
        songs.append(
            Song(i["name"], i["sName"], i["ssName"], i["bpm"], i["key"], i["PC"])
        )
        log(str("Adding Song: " + i["name"]))
    lcd.print("#")

    # Import Effects to Actions Array
    for i in presetFile["actions"]:
        actions.append(FX.action(i["name"], i["type"], i["program"], i["value"], False))
        log(str("Action Action: " + i["name"]))

    lcd.print("#")

    # Import Footswitches
    x = 0
    for i in presetFile["FSAction"]:
        FootSwitches[x].setAction(
            actions[i["action"]], actions[i["holdAction"]]
        )
        x = x + 1
    log(str("Set Up Footswitches"))
    lcd.print("#")

    lcd.set_cursor_pos(3, 10)
    lcd.print("Done!     ")

    currentSongNo = presetFile["currentSong"]
    songNo = currentSongNo

    # GUI Reprint Function
    def PrintGui (l3Mode, FSLine, DeviceMode):
        lcd.print(ui.line0(set, "Live"))
        lcd.print(ui.line1(midiHost, "Live"))
        lcd.print(ui.line2(songs[int(songNo)], "Live"))
        lcd.print(ui.line3(mode, l3Mode, FSLine))

    # Print First GUI
    PrintGui("clear", "Nothing Here", mode)
    log(str("Main UI Printed"))

    # Main Loop
    timePress = 0
    timeSincePress = 0
    cleared = True
    while True:
        # Check for New Song
        songNo = midi.checkSong(currentSongNo)
        if songNo is not currentSongNo:
            try:
                lcd.home()
                PrintGui("clear", (FSin[1]), mode)
                currentSongNo = songNo
            except Exception as e:
                log(str("Change Song Error: " + str(e)))

        # Check For Footswitch Press
        FSin = FX.checkFS(FootSwitches, 0.5)
        if FSin[0] is False:
            timeSincePress = time.monotonic() - timePress
            if (timeSincePress >= 5) and (cleared == False):
                PrintGui("clear", "Nerds", mode)
                log(str("Cleared GUI"))
                cleared = True
            pass
        elif FSin[0] is True:
            timePress = time.monotonic()
            log(str("FS " + FSin[1] + " Pressed"))
            timeSincePress = 0
            lcd.home()
            cleared = False
            PrintGui("loop", (FSin[1]), mode)