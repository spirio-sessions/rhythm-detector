#%%
import wave
from matplotlib import pyplot

from util import read_chunk
from recorder import Recorder
from loader import Loader
from pyaudio import paInt16
from analyser import Analyser

#%%
sample_rate = 44100
chunk_length = 2 #seconds
chunk_size = sample_rate * chunk_length

recorder = Recorder()

wf = wave.open('./recording.wav', 'rb')
chunk = wf.readframes(recorder.chunk_size)
wf.close()

chunk = read_chunk(2, chunk)

analyser = Analyser(recorder.sample_rate, recorder.chunk_length, strength_window_length=0.1)

pyplot.figure()
pyplot.plot(chunk, '.')

smooth = analyser.smooth(chunk)
pyplot.figure()
pyplot.plot(smooth)

window = analyser.window(smooth)
pyplot.figure()
pyplot.plot(window)

flanks = analyser.flanks(window)
pyplot.figure()
pyplot.plot(flanks)

dominant = analyser.dominant(flanks)
pyplot.figure()
pyplot.plot(dominant)

strengths = analyser.strength(window, dominant)
pyplot.figure()
pyplot.plot(strengths)

# %%
sample_rate = 44100
chunk_length = 5.0 #seconds

loader = Loader('/Users/xmaek/Music/Music/Media.localized/Unknown Artist/Unknown Album/Sax_2.wav', chunk_length)
analyser = Analyser(sample_rate, chunk_length)

def callback(chunk):
    smooth = analyser.smooth(chunk)
    pyplot.figure()
    pyplot.plot(smooth)

loader.with_handle(callback).run()
# %%
