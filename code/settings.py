import json
from log import log

try:
    # Load Settings from JSON
    file = open("settings.json", "r")
    settingsFile = json.load(file)
    file.close()
    print(settingsFile)
    if str(settingsFile) == "{}":
        print("empty JSON")
        x = {"firstSetup": True}
        settingsFile = json.dumps(x)
        print(settingsFile)
        file = open("settings.json", "w")
        file.write(settingsFile)
        file.close()
        file = open("settings.json", "r")
        settingsFile = json.load(file)
        file.close()
    log("Imported JSON")
    # Import Presets & Settings
    mode = settingsFile["mode"]
    midiHost = settingsFile["midiHost"]
except Exception as e:
    print("Error: " + str(e))
    log("No Settings File")
    settingsFile = ""
    mode = ""
    midiHost = ""

try:
    file = open("preset.json", "r")
    presetFile = json.load(file)
    file.close()
except Exception as e:
    print("Error: " + str(e))
    presetFile = ""

#liveFile = ""

try:
    file = open("live.json", "r")
    liveFile = json.load(file)
    CC = liveFile["CCStart"]
    file.close()
except Exception as e:
    print("Error: " + str(e))
    CC = ""
    liveFile = ""