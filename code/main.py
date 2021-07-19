from machine import *
import ustruct, gc, utime, json, sys
from time import *
from lcd_driver import I2cLcd
from effects import *
from midi import *
from presets import *

def shutdown (time):
    sleep(time)
    lcd.backlight_off()
    print("off")
    lcd.clear()
    sys.exit()

# Blink LED to confirm Sucessful Boot
activeLED = Pin(25, Pin.OUT)
bootCheck = 0
while bootCheck < 4:
    activeLED.toggle()
    sleep_ms(100)
    activeLED.toggle()
    sleep_ms(100)
    bootCheck+=1

# LCD Setup
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.blink_cursor_off()
lcd.clear()
lcd.hide_cursor()
lcd.backlight_on()

# Footswitch Pin Exaple
"""
FS0 = Pin(3, Pin.IN, Pin.PULL_DOWN)

x = 0
y = 0
lcd.clear()
lcd.putstr(str(x))
FS0Last = 0
while True:
    print("Pin State", FS0.value(), "Loop", y)
    if (FS0Last != FS0.value()) & (FS0.value() == 0):
        x += 1
        lcd.clear()
        lcd.putstr(str(x))
    FS0Last = FS0.value()
    sleep_ms(25)
    y+=1
"""

# Boot Screen
#           --------------------
lcd.putstr("      Midi  Pi      ")
lcd.putstr(" Please set effects ")
lcd.putstr(" to default values  ")
lcd.putstr(" Booting: ")

# Define Footswitches 6-15
FootSwitches = [footSwitch(0, 6), footSwitch(1, 7), footSwitch(2, 8), footSwitch(3, 9), footSwitch(4, 10), footSwitch(5, 11), footSwitch(6, 12), footSwitch(7, 13), footSwitch(8, 14), footSwitch(9, 15)]
lcd.putchar("#")

# Load JSON
file = open("settings.json", 'r')
settings = json.load(file)
file.close()
lcd.putchar("#")
print(settings)
if str(settings) == "{}":
    print("empty JSON")
    x = {"firstSetup": True}
    settings = json.dumps(x)
    print(settings)
    file = open("settings.json", 'w')
    file.write(settings)
    file.close()
    file = open("settings.json", 'r')
    settings = json.load(file)
    file.close()
    

# Import Presets & Settings
songs = []
actions = []
if settings["firstSetup"] == True:
    lcd.clear()
    lcd.putstr("                    ")
    lcd.putstr("    Please Setup    ")
    shutdown(8)
for i in settings["songs"]:
    songs.append(Song(i["name"], i["shortName"], i["sshortName"], i["bpm"], i["PC"]))
lcd.putstr("#")

# Import Effects
for i in settings["actions"]:
    actions.append(action(i["name"], i["type"], i["program"], i["value"]))
lcd.putstr("#")

# Import Footswitches
x = 0
for i in settings["footSwitchesEffects"]:
    FootSwitches[x].setEffect(effects[i["effect"]].toggle(), effects[i["holdEffect"]].toggle(), effects[i["upEffect"]].toggle(), effects[i["rightEffect"]].toggle())
    x = x + 1
lcd.putstr("#")

if settings["mode"] == "Stomp":
    for i in FootSwitches:
        i.setMode(0)
lcd.putstr("#")

lcd.move_to(10, 3)
lcd.putstr("Done!     ")

lcd.clear()

# Main Loop
currentSongNo = settings["currentSong"]
def songLine(line):
    if line == 0:
        songName = songs[currentSongNo].name
        if len(songName) >= 11: songName = songs[currentSongNo].shortName
        if len(songName) >= 11: songName = songName[:11]
        while len(songName) < 11:
            songName = songName + " "
        if len(str(songs[currentSongNo].bpm)) == 3: return songName + " BPM: " + str(songs[currentSongNo].bpm)
        elif len(str(songs[currentSongNo].bpm)) == 2: return songName + " BPM:  " + str(songs[currentSongNo].bpm)
    elif (line == 1) and (currentSongNo != 0):
        songName = songs[currentSongNo-1].name
        if len(songName) >= 5: songName = songs[currentSongNo-1].shortName
        if len(songName) >= 5: songName = songName[:5]
        while len(songName) < 5:
            songName = songName + " "
        if len(str(songs[currentSongNo].bpm)) == 3: return "Prev: " + songName + " BPM: " + str(songs[currentSongNo].bpm)
        elif len(str(songs[currentSongNo].bpm)) == 2: return "Prev: " + songName + " BPM:  " + str(songs[currentSongNo].bpm)
    elif (line == 1): return "  No Previous Song  "
    elif (line == 2):
        try:
            songName = songs[currentSongNo+1].name
            if len(songName) >= 5: songName = songs[currentSongNo+1].shortName
            if len(songName) >= 5: songName = songName[:5]
            while len(songName) < 5:
                songName = songName + " "
            if len(str(songs[currentSongNo].bpm)) == 3: return "Next: " + songName + " BPM: " + str(songs[currentSongNo].bpm)
            elif len(str(songs[currentSongNo].bpm)) == 2: return "Next: " + songName + " BPM:  " + str(songs[currentSongNo].bpm)
        except IndexError: return "    No Next Song    "
    else:
        out = "Mode: " + settings["mode"]
        while len(out) <= 11:
            out = out + " "
        out = out + " Midi Pi"
        return out

lcd.putstr(songLine(0))
lcd.putstr(songLine(1))
lcd.putstr(songLine(2))
lcd.putstr(songLine(3))
x = 0
while x <= 1:
    FSin = checkFS(FootSwitches, 3)
    if FSin == False: pass
    elif FSin == True:
        lcd.clear()
        lcd.putstr("input")
    x = x + 1

shutdown(0)