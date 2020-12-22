#%%
import wave
from matplotlib import pyplot
from numpy import empty, concatenate

from util import read_chunk
from recorder import Recorder
from loader import Loader
from pyaudio import paInt16
from analyser import Analyser

#%%

# perform and plot all analyser steps

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

# analyse recording as block and plot beats over signal

sample_rate = 44100
chunk_length = 5.0 #seconds

loader = Loader('/Users/xmaek/Music/Music/Media.localized/Unknown Artist/Unknown Album/Sax_2.wav', chunk_length)
#loader = Loader('./recording.wav', chunk_length)
analyser = Analyser(sample_rate, chunk_length)

def draw_lines(dominants):
    for i in range(len(dominants)):
        if dominants[i] == 1:
            pyplot.axvline(x=i, color='r')

windowed_signal = empty(0)
dominants_signal = []

def callback(chunk):
    global windowed_signal
    global dominants_signal
    smooth = analyser.smooth(chunk)
    windowed = analyser.window(smooth)
    windowed_signal = concatenate((windowed_signal, windowed))
    dominants_signal += analyser.dominant(analyser.flanks(windowed))

loader.with_handle(callback)
loader.run()

pyplot.figure(figsize=(30,4))
pyplot.plot(windowed_signal)
draw_lines(dominants_signal)
pyplot.xlabel('time in 50ms steps')
pyplot.ylabel('signal amplitude')
pyplot.show()
# %%
