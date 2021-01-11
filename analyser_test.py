#%%
import wave
from matplotlib import pyplot
from numpy import empty, concatenate, mean, sin, pi

from util import read_chunk
from recorder import Recorder
from loader import Loader
from pyaudio import paInt16
from analyser import Analyser


#%%
sample_rate = 48000
window_length = 0.020 #s
hop_length = 0.1 #s

signal = Loader('/Users/xmaek/Music/Music/Media.localized/Unknown Artist/Unknown Album/Sax_1.wav', 0).load()
analyser = Analyser( \
    sample_rate=48000,\
    chunk_length=5.0,\
    window_length=0.25,\
    hop_length=0.05,\
    dominant_window_length=0.5,\
    dominant_hop_length=0.25,\
    dominant_scale=1.0 \
    )
detection_signal = analyser.detect(signal)
peak_signal = analyser.peak_pick(detection_signal)

timestamps = [ i*analyser.hop_length for i in range(len(detection_signal))]

pyplot.figure(figsize=(30,4))
pyplot.plot(timestamps, detection_signal)

for i in range(len(peak_signal)):
    if peak_signal[i] > 0.0:
        pyplot.axvline(x=i*analyser.hop_length, color='r')

pyplot.show()
# %%