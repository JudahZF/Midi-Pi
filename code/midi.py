import time, board, busio, adafruit_midi, usb_midi
from log import log
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.program_change import ProgramChange
from settings import liveFile

uart = busio.UART(board.GP0, board.GP1, baudrate=31250, timeout=0.001)  # init UART
midi_in_channel = 1
midi_out_channel = 1
midi0 = adafruit_midi.MIDI(
    midi_in=uart,
    midi_out=uart,
    in_channel=(midi_in_channel - 1),
    out_channel=(midi_out_channel - 1),
    debug=False,
    )

midi1 = adafruit_midi.MIDI(midi_out=usb_midi.ports[0],midi_in=usb_midi.ports[0], out_channel=0, in_channel=4)
midi = midi0
def setupMidi(mode):
    if mode.upper() == "MIDI":
        midi = midi0
    elif mode.upper() == "USB":
        midi = midi1

def sendCC(program, value):
    midi.send(ControlChange(program, value))

def sendPC(program):
    midi.send(ProgramChange(program))

# Check CC 3 For SOng Change
def checkSong(CurrentSong, mode):
    midiIn = midi.receive()
    if mode == "Preset":
        songNo = CurrentSong
        try:
            if midiIn.control is 3: 
                songNo = midiIn.value
        except Exception:
            print("Error")
        return songNo
    if mode == "Live":
        songName = []
        try: song = CurrentSong[0]
        except Exception: song = ""
        try: bpm = CurrentSong[2]
        except Exception: bpm = 120
        try: key = CurrentSong[1]
        except Exception: key = ""
        try: currentPart = CurrentSong[3]
        except Exception: currentPart = ""
        try: nextPart = CurrentSong[3]
        except Exception: nextPart = ""
        """try:
            if (midiIn.note == 5) & (midiIn.velocity > 0):
                pass
        except Exception as e:
            if str(e) != "'NoneType' object has no attribute 'note'":
                log(str(e))
            return CurrentSong"""
        if midiIn.note == 1:
            velocity = midiIn.velocity
            while velocity == 127:
                midiIn = midi.receive()
                """try:
                    if ((midiIn.note <= 3 or ((12 <= midiIn.note) & (midiIn.note <= 23))) & (midiIn.velocity > 0)): 
                        pass
                except Exception as e:
                    if str(e) != "'NoneType' object has no attribute 'note'":
                        log(str(e))
                    continue"""
                match midiIn.note:
                    case 0:
                        try:
                            song = ""
                            midiChar = chr(midiIn.velocity)
                            songName.append(midiChar)
                        except Exception as e:
                            if str(e) != "'NoteOff' object has no attribute 'velocity'":
                                log(str(e))
                            pass
                    case 3: bpm = midiIn.velocity
                    case 2: bpm += (128^midiIn.velocity)-1
                    case 12: key = "C"
                    case 13: key = "C#"
                    case 14: key = "D"
                    case 15: key = "D#"
                    case 16: key = "E"
                    case 17: key = "F"
                    case 18: key = "F#"
                    case 19: key = "G"
                    case 20: key = "G#"
                    case 21: key = "A"
                    case 22: key = "A#"
                    case 23: key = "B"
                    case 5: currentPart = str(liveFile['parts'][midiIn.velocity-1])
                    case 4: currentPart = currentPart + ";" + str(midiIn.velocity)
                    case 8: nextPart = str(liveFile['parts'][midiIn.velocity-1])
                    case 7: nextPart = nextPart + ";" + str(midiIn.velocity)
                    case 1: velocity = midiIn.velocity
            song = songName.join()
        log(str(song))
        log(str(bpm))
        log(str(key))
        log(str(currentPart))
        log(str(nextPart))
        return song, key, bpm, currentPart, nextPart