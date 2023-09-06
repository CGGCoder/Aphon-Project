# +------------------------+
# |    Aphon Gen X V0.1    |
# +------------------------+

# ---------------------------------------------------------------------------------\
# PARAMS > To set a parameter: parameter = value                                   |
# AUDIO > To play a note: MODE sxxx/txx.xx/bxx.xx.xx xxx xxx sxxx/txx.xx/bxx.xx.xx |
#                                v                    |   v        |               |
#         Time in samples, seconds or beats           v   Volume   |               |
#               (sxxx/tss.ms/bmm.bb.sb)       Pitch (Hz)  (0-100)  v               |
#                      v          |   Length in samples, seconds or beats          |
#           seconds.milliseconds  v                  (sxxx/tss.ms/bmm.bb.sb)       |
#                        measure.beat.sub-beat                                     |
# ---------------------------------------------------------------------------------/

# Packages
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import math

Tk().withdraw()

# Variables
pitch_chars = {'C0':       16.35, 'C#/Db0':   17.32, 'D0':       18.35, 'D#/Eb0':   19.45, 'E0':       20.60, 'F0':   21.83, 
               'F#/Gb0':   23.12, 'G0':       24.50, 'G#/Ab0':   25.96, 'A0':       27.50, 'A#/Bb0':   29.14, 'B0':   30.87, 
               'C1':       32.70, 'C#/Db1':   34.65, 'D1':       36.71, 'D#/Eb1':   38.89, 'E1':       41.20, 'F1':   43.65, 
               'F#/Gb1':   46.25, 'G1':       49.00, 'G#/Ab1':   51.91, 'A1':       55.00, 'A#/Bb1':   58.27, 'B1':   61.74, 
               'C2':       65.41, 'C#/Db2':   69.30, 'D2':       73.42, 'D#/Eb2':   77.78, 'E2':       82.41, 'F2':   87.31, 
               'F#/Gb2':   92.50, 'G2':       98.00, 'G#/Ab2':  103.83, 'A2':      110.00, 'A#/Bb2':  116.54, 'B2':  123.47, 
               'C3':      130.81, 'C#/Db3':  138.59, 'D3':      146.83, 'D#/Eb3':  155.56, 'E3':      164.81, 'F3':  174.61,
               'F#/Gb3':  185.00, 'G3':      196.00, 'G#/Ab3':  207.65, 'A3':      220.00, 'A#/Bb3':  233.08, 'B3':  246.94, 
               'C4':      261.63, 'C#/Db4':  277.18, 'D4':      293.66, 'D#/Eb4':  311.13, 'E4':      329.63, 'F4':  349.23, 
               'F#/Gb4':  369.99, 'G4':      392.00, 'G#/Ab4':  415.30, 'A4':      440.00, 'A#/Bb4':  466.16, 'B4':  493.88, 
               'C5':      523.25, 'C#/Db5':  554.37, 'D5':      587.33, 'D#/Eb5':  622.25, 'E5':      659.25, 'F5':  698.46, 
               'F#/Gb5':  739.99, 'G5':      783.99, 'G#/Ab5':  830.61, 'A5':      880.00, 'A#/Bb5':  932.33, 'B5':  987.77, 
               'C6':     1046.50, 'C#/Db6': 1108.73, 'D6':     1174.66, 'D#/Eb6': 1244.51, 'E6':     1318.51, 'F6': 1396.91, 
               'F#/Gb6': 1479.98, 'G6':     1567.98, 'G#/Ab6': 1661.22, 'A6':     1760.00, 'A#/Bb6': 1864.66, 'B6': 1975.53, 
               'C7':     2093.00, 'C#/Db7': 2217.46, 'D7':     2349.32, 'D#/Eb7': 2489.02, 'E7':     2637.02, 'F7': 2793.83, 
               'F#/Gb7': 2959.96, 'G7':     3135.96, 'G#/Ab7': 3322.44, 'A7':     3520.00, 'A#/Bb7': 3729.31, 'B7': 3951.07, 
               'C8':     4186.01, 'C#/Db8': 4434.92, 'D8':     4698.63, 'D#/Eb8': 4978.03, 'E8':     5274.04, 'F8': 5587.65, 
               'F#/Gb8': 5919.91, 'G8':     6271.93, 'G#/Ab8': 6644.88, 'A8':     7040.00, 'A#/Bb8': 7485.62, 'B8': 7902.13}
params = {"TEMPO":120, "BEATS/MEASURE":4}
file_in = "Instructions.txt"
file_out = "Output.wav"
pitch_file = "12TETPitches.txt"
temp = None

# For the moment, it uses a sine wave. (It will soon be capable of using different sounds)
# MODES:
# REP > Default Mode/Replace Mode, overwrites values in file
# ADD > Addition Mode, adds to existing values in file
def write_note(start_time = 0, pitch = 1, volume = 0, length = 0, mode = "REP"):
    if pitch <= 0:
        return None
    with open(file_out, "r+b") as fout:
        fout.seek(44+start_time)
        print(start_time/44100, pitch, volume/100, length/44100)
        for l in range(length+1):
            calc_pitch = round((volume*327.67)*math.sin(2*pitch*l*math.pi/44100))
            if mode == "REP":
                fout.write(calc_pitch.to_bytes(2, byteorder='little', signed=True))
            elif mode == "ADD":
                temp = int.from_bytes(fout.read(2), byteorder='little',signed=True)
                fout.seek(-2, 1)
                temp = (calc_pitch+temp)//2
                if temp > 32767:
                    temp = 32767
                if temp < -32768:
                    temp = -32768
                fout.write(temp.to_bytes(2, byteorder='little', signed=True))
        print(l/44100, (l+start_time)/44100)

# Check What Offset/Size
# SubChunk2Size  40/4  =  (In this case) NumSamples
# ChunkSize       4/4  =  36 + SubChunk2Size
def correct_audio_file():
    with open(file_out, "r+b") as fcheck:
        fcheck.seek(44)
        temp = fcheck.read()
        temp = fcheck.tell()-44
        fcheck.seek(40)
        fcheck.write(temp.to_bytes(4, byteorder='little'))
        fcheck.seek(4)
        temp += 36
        fcheck.write(temp.to_bytes(4, byteorder='little'))
        fcheck.seek(0)
        fcheck.write(b'\x52\x49\x46\x46')
        fcheck.seek(8)
        fcheck.write(b'\x57\x41\x56\x45\x66\x6D\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00\x44\xAC\x00\x00\x88\x58\x01\x00\x02\x00\x10\x00\x64\x61\x74\x61')

def clear_file(file = "Output.wav"):
    with open(file, "w"):
        pass

# MODES:
# DEF > Default Mode, does nothing
# PARAMETERS > PARAMS > Parameter Mode, enters parameters
# BEGIN > AUDIO > Note/Input Mode, processes notes into audio
def parse_file():
    mode = "DEF"
    with open(file_in, "r") as fin:
        for line in fin:
            audio_mode = "REP"
            line = line[:-1]
            if not line:
                continue
            if line[:4] == "ADD ":
                audio_mode = "ADD"
                line = line[4:]
            if line[0] == "#":
                continue
            if line == "PARAMETERS":
                mode = "PARAMS"
                continue
            elif line == "BEGIN":
                mode = "AUDIO"
                continue
            elif line == "CLEAR":
                clear_file(file_out)
                continue
            if mode == "PARAMS":
                temp = line.split(" = ")
                if temp[0].upper() in params:
                    params[temp[0].upper()] = temp[1]
                continue
            if mode == "AUDIO":
                temp = line.split(" ")
                parse_audio_line(temp, audio_mode)
    correct_audio_file()

def parse_audio_line(line = 0, mode = "REP"):
    start, pitch, volume, length = line
    if start[0] == "s":
        start = int(start[1:])
    elif start[0] == "t":
        start = convert_time_to_samples(float(start[1:]))
    elif start[0] == "b":
        temp = start[1:].split(".",1)
        start = convert_beats_to_samples(int(temp[0]), float(temp[1]))
    if length[0] == "s":
        length = int(length[1:])
    elif length[0] == "t":
        length = convert_time_to_samples(float(length[1:]))
    elif length[0] == "b":
        temp = length[1:].split(".",1)
        length = convert_beats_to_samples(int(temp[0]), float(temp[1]))
    try:
        pitch = float(pitch)
    except:
        pitch = convert_pitch(pitch)
    volume = float(volume)
    write_note(start, pitch, volume, length, mode)

def convert_time_to_samples(value = 0):
    return round(value*44100)

def convert_beats_to_samples(measure = 0, beats = 0.0):
    tempo = int(params["TEMPO"])
    beats_per_measure = int(params["BEATS/MEASURE"])
    return round((measure*beats_per_measure+beats)*2646000/tempo)

def convert_pitch(pitch = "C4"):
    pitch_letter = "A"
    if pitch[1] == "#":
        if pitch[0] == "G":
            pitch_letter = "A"
        else:
            pitch_letter = chr(ord(pitch[0])+1)
        pitch = pitch[0]+"#/"+pitch_letter+"b"+pitch[2]
    elif pitch[1] == "b":
        if pitch[0] == "A":
            pitch_letter = "G"
        else:
            pitch_letter = chr(ord(pitch[0])-1)
        pitch = pitch_letter+"#/"+pitch[0]+"b"+pitch[2]
    return pitch_chars[pitch]


# Main Program
if __name__ == "__main__":
# file_in = askopenfilename(title="Open Input")
# file_out = askopenfilename(title="Open Output")
    print("Converting...")
    parse_file()
    print("Done!")
