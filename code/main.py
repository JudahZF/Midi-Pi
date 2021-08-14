import json
import sys
import busio
import time
import digitalio
import effects as FX
import presets
import usb_midi
import ui
import midi
import board
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lcd.lcd import CursorMode

lcd = LCD(I2CPCF8574Interface(busio.I2C(scl=board.GP3, sda=board.GP2), 0x27))
lcd.set_cursor_mode(CursorMode.HIDE)

def shutdown(wait):
    time.sleep(wait)
    lcd.set_backlight(False)
    print("off")
    lcd.clear()
    sys.exit()

# Blink LED to confirm Sucessful Boot
activeLED = digitalio.DigitalInOut(board.GP25)
activeLED.direction = digitalio.Direction.OUTPUT
bootCheck = 0
while bootCheck < 4:
    activeLED.value = True
    time.sleep(0.100)
    activeLED.value = False
    time.sleep(0.100)
    bootCheck += 1

# Boot Screen
lcd.print("      Midi  Pi      ")
lcd.print(" Please set effects ")
lcd.print(" to default values  ")
lcd.print(" Booting: ")

# Define Footswitches 6-15
FootSwitches = [
    FX.footSwitch(0, board.GP4),
    FX.footSwitch(1, board.GP5),
    FX.footSwitch(2, board.GP6),
    FX.footSwitch(3, board.GP7),
    FX.footSwitch(4, board.GP8),
    FX.footSwitch(5, board.GP9),
    FX.footSwitch(6, board.GP10),
    FX.footSwitch(7, board.GP11),
    FX.footSwitch(8, board.GP12),
    FX.footSwitch(9, board.GP13),
]
lcd.print("#")
# Load JSON
file = open("settings.json", "r")
settings = json.load(file)
file.close()
lcd.print("#")
print(settings)
if str(settings) == "{}":
    print("empty JSON")
    x = {"firstSetup": True}
    settings = json.dumps(x)
    print(settings)
    file = open("settings.json", "w")
    file.write(settings)
    file.close()
    file = open("settings.json", "r")
    settings = json.load(file)
    file.close()


# Import Presets & Settings
songs = []
actions = []
mode = settings["mode"]
set = settings["Set Name"]
midiHost = settings["midiHost"]
if (settings["firstSetup"] is True):
    lcd.clear()
    lcd.print("                    ")
    lcd.print("    Please Setup    ")
    shutdown(8)
for i in settings["songs"]:
    songs.append(
        presets.Song(i["name"], i["sName"], i["ssName"], i["bpm"], i["key"], i["PC"])
    )
lcd.print("#")

# Import Effects
for i in settings["actions"]:
    actions.append(FX.action(i["name"], i["type"], i["program"], i["value"], False))
midi.setupMidi(settings["midiHost"])
lcd.print("#")

# Import Footswitches
x = 0
for i in settings["FSAction"]:
    FootSwitches[x].setAction(
        actions[i["action"]], actions[i["holdAction"]]
    )
    print(str(FootSwitches[x].tapAction))
    x = x + 1
lcd.print("#")

# Setup Custom Chars
lcd.create_char(0, bytearray([0x00, 0x04, 0x08, 0x1F, 0x08, 0x04, 0x00, 0x00]))  # Prev
lcd.create_char(1, bytearray([0x00, 0x04, 0x02, 0x1F, 0x02, 0x04, 0x00, 0x00]))  # Next
lcd.create_char(2, bytearray([0x00, 0x0E, 0x0A, 0x0E, 0x04, 0x06, 0x06, 0x00]))  # Key
lcd.print("#")

lcd.set_cursor_pos(3, 10)
lcd.print("Done!     ")

currentSongNo = settings["currentSong"]

# Main Loop
def PrintGui (l3Mode, FSLine, DeviceMode):
    if DeviceMode == "Stomp":
        lcd.print(ui.line0(songs[currentSongNo], "Both"))
        lcd.print(ui.line1(songs[int(currentSongNo - 1)], "Both"))
        lcd.print(ui.line2(songs[int(currentSongNo + 1)], "Both"))
        lcd.print(ui.line3(mode, l3Mode, FSLine))
    elif DeviceMode == "Live":
        lcd.print(ui.line0(set, "Live"))
        lcd.print(ui.line1(midiHost, "Live"))
        lcd.print(ui.line2(songs[int(currentSongNo + 1)], "Both"))
        lcd.print(ui.line3(mode, l3Mode, FSLine))

print(time.monotonic())
PrintGui("clear", "Nothing Here", mode)
timePress = 0
timeSincePress = 0
while True:
    FSin = FX.checkFS(FootSwitches, 0.5)
    time.sleep(0.01)
    print(midi.checkSong())
    if FSin[0] is False:
        timeSincePress = time.monotonic() - timePress
        if timeSincePress == 14400000:
            shutdown(10)
        if timeSincePress <= 60000:
            PrintGui("clear", "Nerds", mode)
        pass
    elif FSin[0] is True:
        timePress = time.monotonic()
        timeSincePress = 0
        lcd.home()
        PrintGui("loop", (FSin[1]), mode)



# Shutdown
"""if FSin[2] == 0:
    shutdown(8)"""
