def addBPM(song, line):
    if len(str(song.bpm)) == 2:
        line = line + " T: " + str(song.bpm)
    elif len(str(song.bpm)) == 3:
        line = line + " T:" + str(song.bpm)
    return line


def addKey(song, line):
    if len(str(song.key)) == 1:
        line = line + " " + chr(2) + ":" + str(song.key) + " "
    elif len(str(song.key)) == 2:
        line = line + " " + chr(2) + ":" + str(song.key)
    return line


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
    elif displayMode == "Live":
        setName = text[:20]
        if len(setName) < 20:
            setName = " " + setName
        while len(setName) < 20:
            setName = setName + " "
        line = setName
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
        line = chr(0) + " " + songName
        line = addKey(text, line)
        line = addBPM(text, line)
        return line
    elif displayMode == "Live":
        line = "Midi Mode: " + text[:9]
        while 20 > len(line):
            line = line + " "
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
    elif displayMode == "Live":
        line = "Track: " + shortenName(text, 13)
        while 20 > len(line):
            line = line + " "
        return line



def line3(mode, displayMode, FSLine):
    line = ""
    if displayMode == "clear":
        line = "Mode:" + mode
        while 11 >= len(line):
            line = line + " "
        line = line + " Midi Pi"
    elif displayMode == "loop":
        line = "Mode:" + mode[:1]
        while 6 >= len(line):
            line = line + " "
        while 12 >= len(FSLine):
           FSLine = " " + FSLine
        line = line + FSLine
    return line
