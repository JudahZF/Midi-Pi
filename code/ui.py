# Add BPM to end of string
def addBPM(song, line):
    if len(str(song.bpm)) == 2:
        line = line + " T: " + str(song.bpm)
    elif len(str(song.bpm)) == 3:
        line = line + " T:" + str(song.bpm)
    return line

# Add Key to end of string
def addKey(song, line):
    if len(str(song.key)) == 1:
        line = line + " " + chr(2) + ":" + str(song.key) + " "
    elif len(str(song.key)) == 2:
        line = line + " " + chr(2) + ":" + str(song.key)
    return line

# Shorten Song Name
def shortenName(song, length):
    leng = length
    songName = song.name
    if len(songName) >= leng:
        songName = song.shortName
    if (len(songName) >= leng) and (8 >= leng):
        songName = song.sshortName
    if len(songName) >= leng:
        songName = songName[:leng]
    while len(songName) < leng:
        songName = songName + " "
    return songName


# Function for Generating each line on the LCD (for 20x4 display)

def line0(text, displayMode):
    if displayMode == "BPM":
        songName = shortenName(text, 11)
        line = songName
        line = addBPM(text, line)
        return line
    elif displayMode == "Key":
        songName = shortenName(text, 12)
        line = songName
        line = addKey(text, line)
        return line
    elif displayMode == "Both":
        songName = shortenName(text, 9)
        line = songName
        line = addKey(text, line)
        line = addBPM(text, line)
        return line
    elif displayMode == "Preset":
        setName = text[:20]
        if len(setName) < 20:
            setName = " " + setName
        while len(setName) < 20:
            setName = setName + " "
        line = setName
        return line
    elif displayMode == "Live":
        songName = text[:14]
        line = "Song: " + songName
        line = line + " "*(20-len(line))
        return line

def line1(text, displayMode):
    if displayMode == "BPM":
        songName = shortenName(text, 9)
        line = chr(0) + " " + songName
        line = addBPM(text, line)
        return line
    elif displayMode == "Key":
        songName = shortenName(text, 10)
        line = chr(0) + " " + songName
        line = addKey(text, line)
        return line
    elif displayMode == "Both":
        songName = shortenName(text, 7)
        line = "C " + songName
        line = addKey(text, line)
        line = addBPM(text, line)
        return line
    elif displayMode == "Preset":
        line = "Midi Mode: " + text[:9]
        while 20 > len(line):
            line = line + " "
        return line
    elif displayMode == "Live":
        keyBPM = text.split(":")
        line = "Key: " + keyBPM[0] 
        line = line + " "*(10-len(line))
        line = line + "BPM: " + keyBPM[1]
        line = line + " "*(20-len(line))
        return line

def line2(text, displayMode):
    if displayMode == "BPM":
        songName = shortenName(text, 9)
        line = chr(1) + " " + songName
        line = addBPM(text, line)
        return line
    elif displayMode == "Key":
        songName = shortenName(text, 10)
        line = chr(1) + " " + songName
        line = addKey(text, line)
        return line
    elif displayMode == "Both":
        songName = shortenName(text, 7)
        line = chr(1) + " " + songName
        line = addKey(text, line)
        line = addBPM(text, line)
        return line
    elif displayMode == "Preset":
        line = "Midi Mode: " + text[:9]
        while 20 > len(line):
            line = line + " "
        return line
    elif displayMode == "Live":
        parts = text.split(":")
        current = parts[0].split(";")
        next = parts[1].split(";")
        if len(current) == 2: currentLine = "C:" + current[0][:6] + " " + current[1][:1] + " "*(8-len(current[0][:6] + " " + current[1][:1]))
        elif len(current) == 1: currentLine = "C:" + current[0][:8] + " "*(8-len(current[0][:8]))
        if len(next) == 2: nextLine = chr(1) + ":" + next[0][:6] + " " + next[1][:1] + " "*(8-len(next[0][:6] + " " + next[1][:1]))
        elif len(next) == 1: nextLine = chr(1) + ":" + next[0][:8] + " "*(8-len(next[0][:8]))
        line = currentLine + nextLine
        return line

def line3(mode, displayMode, FSLine):
    line = ""
    if displayMode == "loop":
        line = "Mode: " + mode[:1]
        while 6 >= len(line):
            line = line + " "
        while 12 >= len(FSLine):
           FSLine = " " + FSLine
        line = line + FSLine
    else:
        line = "Mode: " + mode
        while 11 >= len(line):
            line = line + " "
        line = line + " Midi Pi"
    return line
