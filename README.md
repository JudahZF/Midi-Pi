# Midi Pi V2
A midi controller based on CircuitPython and the Raspberry Pi Pico

## How to setup: 
First flash your Pico Pi with (Circuit Python)[https://circuitpython.org/board/raspberry_pi_pico/]
Then download the latest release and copy it to the Circuit Python drive.
Finally open settings.json and edit the config as needed

## Current Features:

- [] Modes:
  - [x] Preset Mode
    - Allows displaying of predefined songs in the preset.json, that sync with a midi cc.
  - [ ] Live
    - Recieves all displayed information via midi notes.

## To Do

- [ ] Create Live Mode
  - [x] Program UI
  - [x] Program Midi Receiving
  - [ ] Program FS
  - [ ] Create Midi Clips
- [ ] Program Editor
