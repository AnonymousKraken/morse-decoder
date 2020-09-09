import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile
from scipy.signal import savgol_filter
from scipy.fftpack import fft, fftfreq

morseCodeLetters = {
    ".-"   : "a",
    "-..."  : "b",
    "-.-." : "c",
    "-.."  : "d",
    "."    : "e",
    "..-." : "f",
    "--."  : "g",
    "...." : "h",
    ".."   : "i",
    ".---" : "j",
    "-.-"  : "k",
    ".-.." : "l",
    "--"   : "m",
    "-."   : "n",
    "---"  : "o",
    ".--." : "p",
    "--.-" : "q",
    ".-."  : "r",
    "..."  : "s",
    "-"    : "t",
    "..-"  : "u",
    "...-" : "v",
    ".--"  : "w",
    "-..-" : "x",
    "-.--" : "y",
    "--.." : "z",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    "-....": "5",
    "--...": "6",
    "---..": "7",
    "----.": "8",
    "-----": "0"
}

farnsworthTiming = (1,3,1,3,7)
amplitudeThreshold = 5000

samplerate, audio = wavfile.read("actual-morse-small.wav")

# Convert audio into boolean values for each sample
data = []
for i in range(len(audio)):
    for sample in audio[i-100:i+100]:
        if sample > amplitudeThreshold:
            data.append(True)
            break
    else:
        data.append(False)

plt.plot(data)
plt.show()

# Convert boolean values into timing data for how long the signal is high/low
timingData = []
currentCount = 0
for i in range(len(data)-1):
    if data[i] == data[i+1]:
        currentCount += 1
    else: 
        timingData.append((data[i], currentCount))
        currentCount = 0

# Remove initial silence
if timingData[0][0] == False:
    timingData.pop(0)

# Convert time in samples to time in units 
unitLength = min([x[1] for x in timingData])
unitData = [(x[0], round(x[1]/unitLength)) for x in timingData] + [(False, 1)]

print(unitData)

# Convert signals into letters and words
currentLetter = ""
output = ""
for signal in unitData:
    if signal[0] == True: # If dit or dah
        if signal[1] <= 2:
            currentLetter += "."
        else:
            currentLetter += "-"
    else: 
        if signal[1] >= 3: # If letter break
            try:
                output += morseCodeLetters[currentLetter]
            except KeyError:
                output += "?"
            currentLetter = ""
        if signal[1] == 7: # If word break
            output += " "

print(output)