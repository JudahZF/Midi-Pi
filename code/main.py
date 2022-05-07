from settings import settingsFile, mode, midiHost, presetFile, CC
import busio, board, digitalio, json, sys, time, usb_midi, ui, midi, presets, live, performance
import effects as FX
from log import log
from lcd.lcd import LCD
from lcd.i2c_pcf8574_interface import I2CPCF8574Interface
from lcd.lcd import CursorMode
 
# Setup LCD
lcd = LCD(I2CPCF8574Interface(busio.I2C(scl=board.GP3, sda=board.GP2), 0x27))
lcd.set_cursor_mode(CursorMode.HIDE)

if settingsFile == "":
    lcd.clear()
    lcd.print("Add a settings file")
    time.sleep(30)
    lcd.clear()
    sys.exit()

# Setup Custom Chars
lcd.create_char(0, bytearray([0x00, 0x04, 0x08, 0x1F, 0x08, 0x04, 0x00, 0x00]))  # Prev
lcd.create_char(1, bytearray([0x00, 0x04, 0x02, 0x1F, 0x02, 0x04, 0x00, 0x00]))  # Next
lcd.create_char(2, bytearray([0x00, 0x0E, 0x0A, 0x0E, 0x04, 0x06, 0x06, 0x00]))  # Key
log(str("Set Up Custom Characters"))

# Shutdown Function
def shutdown(wait):
    time.sleep(wait)
    lcd.set_backlight(False)
    log(str("Shutdown"))
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
  # FX.footSwitch(Footswitch Number, GPIO Pin Number),
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

# Check for firstime Setup
if (settingsFile["firstSetup"] is True):
    lcd.clear()
    lcd.print("                    ")
    lcd.print("    Please Setup    ")
    log("SYSTEM NOT SETUP")
    shutdown(8)

# Set Midi Mode
midi.setupMidi(midiHost)
log(str("Set Up Midi: " + midiHost))
lcd.print("#")
if mode == "Preset":
    run = presets.mode(lcd, presetFile, FootSwitches, midiHost)
elif mode == "Live":
    run = live.mode(lcd, presetFile, FootSwitches, midiHost, CC)
elif mode == "Perf":
    run = performance.mode(lcd, presetFile, FootSwitches, midiHost, CC)
run.run()