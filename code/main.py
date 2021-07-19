import json
import sys
import busio
import time
import digitalio
import effects as FX
import presets
import ui
import board
import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd

print("help")
# LCD Setup
# i2c setup, higher frequency for display refresh
lcd_columns = 20
lcd_rows = 4
i2c = busio.I2C(board.GP3, board.GP2)
#  i2c display setup
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows)


def shutdown(wait):
    time.sleep(wait)
    lcd.backlight_off()
    print("off")
    lcd.clear()
    sys.exit()

# Blink LED to confirm Sucessful Boot
activeLED = digitalio.DigitalInOut(board.GP25)
bootCheck = 0
while bootCheck < 4:
    activeLED.toggle()
    time.sleep_ms(100)
    activeLED.toggle()
    time.sleep_ms(100)
    bootCheck += 1

# Boot Screen
lcd.message("      Midi  Pi      ")
lcd.message(" Please set effects ")
lcd.message(" to default values  ")
lcd.message(" Booting: ")

# Define Footswitches 6-15
FootSwitches = [
    FX.footSwitch(0, 6),
    FX.footSwitch(1, 7),
    FX.footSwitch(2, 8),
    FX.footSwitch(3, 9),
    FX.footSwitch(4, 10),
    FX.footSwitch(5, 11),
    FX.footSwitch(6, 12),
    FX.footSwitch(7, 13),
    FX.footSwitch(8, 14),
    FX.footSwitch(9, 15),
]
lcd.putchar("#")

# Load JSON
file = open("settings.json", "r")
settings = json.load(file)
file.close()
lcd.putchar("#")
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
if (settings["firstSetup"] is True):
    lcd.clear()
    lcd.message("                    ")
    lcd.message("    Please Setup    ")
    shutdown(8)
for i in settings["songs"]:
    songs.append(
        presets.Song(i["name"], i["sName"], i["ssName"], i["bpm"], i["key"], i["PC"])
    )
lcd.message("#")

# Import Effects
for i in settings["actions"]:
    FX.actions.append(FX.action(i["name"], i["type"], i["program"], i["value"]))
lcd.message("#")

# Import Footswitches
x = 0
for i in settings["FSAction"]:
    FootSwitches[x].setAction(
        actions[i["action"]].toggle(), actions[i["holdAction"]].toggle()
    )
    x = x + 1
lcd.message("#")

# Setup Custom Chars
lcd.create_char(0, bytearray([0x00, 0x04, 0x08, 0x1F, 0x08, 0x04, 0x00, 0x00]))  # Prev
lcd.create_char(1, bytearray([0x00, 0x04, 0x02, 0x1F, 0x02, 0x04, 0x00, 0x00]))  # Next
lcd.create_char(2, bytearray([0x00, 0x0E, 0x0A, 0x0E, 0x04, 0x06, 0x06, 0x00]))  # Key
lcd.putstr("#")

lcd.move_to(10, 3)
lcd.putstr("Done!     ")

currentSongNo = settings["currentSong"]

# Main Loop
lcd.putstr(ui.line0(songs[currentSongNo], "Both"))
lcd.putstr(ui.line1(songs[int(currentSongNo - 1)], "Both"))
lcd.putstr(ui.line2(songs[int(currentSongNo + 1)], "Both"))
lcd.putstr(ui.line3(mode))

x = 0
while x <= 1:
    FSin = FX.checkFS(FootSwitches, 3)
    if FSin is False:
        pass
    elif FSin is True:
        lcd.clear()
        lcd.putstr("input")
    x = x + 1

shutdown(10)
