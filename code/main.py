import gc, json, sys, busio
from time import *
from effects import *
from midi import *
from presets import *
from ui import *

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
# i2c setup, higher frequency for display refresh
i2c = busio.I2C(board.GP1, board.GP0, frequency=1000000)
#  i2c display setup
display_bus = displayio.I2CDisplay(i2c, device_address=0x3D)


# Boot Screen
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
mode = settings["mode"]
if settings["firstSetup"] == True:
    lcd.clear()
    lcd.putstr("                    ")
    lcd.putstr("    Please Setup    ")
    shutdown(8)
for i in settings["songs"]:
    songs.append(Song(i["name"], i["shortName"], i["sshortName"], i["bpm"], i["key"], i["PC"]))
lcd.putstr("#")

# Import Effects
for i in settings["actions"]:
    actions.append(action(i["name"], i["type"], i["program"], i["value"]))
lcd.putstr("#")

# Import Footswitches
x = 0
for i in settings["FSAction"]:
    FootSwitches[x].setAction(actions[i["action"]].toggle(), actions[i["holdAction"]].toggle())
    x = x + 1
lcd.putstr("#")

# Setup Custom Chars
lcd.custom_char(0, bytearray([0x00, 0x04, 0x08, 0x1F, 0x08, 0x04, 0x00, 0x00])) # Prev
lcd.custom_char(1, bytearray([0x00, 0x04, 0x02, 0x1F, 0x02, 0x04, 0x00, 0x00])) # Next
lcd.custom_char(2, bytearray([0x00, 0x0E, 0x0A, 0x0E, 0x04, 0x06, 0x06, 0x00]))
lcd.putstr("#")

lcd.move_to(10, 3)
lcd.putstr("Done!     ")

currentSongNo = settings["currentSong"]

# Main Loop
lcd.putstr(line0(songs[currentSongNo], "Both"))
lcd.putstr(line1(songs[int(currentSongNo-1)], "Both"))
lcd.putstr(line2(songs[int(currentSongNo+1)], "Both"))
lcd.putstr(line3(mode))

x = 0
while x <= 1:
    FSin = checkFS(FootSwitches, 3)
    if FSin == False: pass
    elif FSin == True:
        lcd.clear()
        lcd.putstr("input")
    x = x + 1

shutdown(10)