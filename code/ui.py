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


def line0(song, displayMode):
    if displayMode == "BPM":
        songName = shortenName(song, 11)
        line = songName
        line = addBPM(song, line)
        return line
    elif displayMode == "Key":
        songName = shortenName(song, 12)
        line = songName
        line = addKey(song, line)
        return line
    elif displayMode == "Both":
        songName = shortenName(song, 9)
        line = songName
        line = addKey(song, line)
        line = addBPM(song, line)
        return line


def line1(song, displayMode):
    if displayMode == "BPM":
        songName = shortenName(song, 9)
        line = chr(0) + " " + songName
        line = addBPM(song, line)
        return line
    elif displayMode == "Key":
        songName = shortenName(song, 10)
        line = chr(0) + " " + songName
        line = addKey(song, line)
        return line
    elif displayMode == "Both":
        songName = shortenName(song, 7)
        line = chr(0) + " " + songName
        line = addKey(song, line)
        line = addBPM(song, line)
        return line


def line2(song, displayMode):
    if displayMode == "BPM":
        songName = shortenName(song, 9)
        line = chr(1) + " " + songName
        line = addBPM(song, line)
        return line
    elif displayMode == "Key":
        songName = shortenName(song, 10)
        line = chr(1) + " " + songName
        line = addKey(song, line)
        return line
    elif displayMode == "Both":
        songName = shortenName(song, 7)
        line = chr(1) + " " + songName
        line = addKey(song, line)
        line = addBPM(song, line)
        return line


def line3(mode):
    line = "Mode:" + mode
    while 11 >= len(line):
        line = line + " "
    line = line + " Midi Pi"
    return line
