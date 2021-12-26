import json
from main import lcd

try:
    file = open("settings.json", "r")
    settingsFile = json.load(file)
    file.close()
except Exception as e:
    print("Error: " + e)
    lcd.print("Please add a Settings file!")

try:
    file = open("preset.json", "r")
    presetFile = json.load(file)
    file.close()
except Exception as e:
    print("Error: " + e)