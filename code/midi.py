import time
import board
import busio
import adafruit_midi
import usb_midi
from adafruit_midi.control_change import ControlChange
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.program_change import ProgramChange

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

def setupMidi(mode):
    if mode == "MIDI":
        uart = busio.UART(board.GP1, board.GP0, baudrate=31250, timeout=0.001)  # init UART
        midi_in_channel = 2
        midi_out_channel = 1
        midi0 = adafruit_midi.MIDI(
            midi_in=uart,
            midi_out=uart,
            in_channel=(midi_in_channel - 1),
            out_channel=(midi_out_channel - 1),
            debug=False,
        )
    elif mode == "USB":
        midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)

def sendCC(program, value):
    midi.send(ControlChange(program, value))

def sendPC(program):
    midi.send(ProgramChange(program))
