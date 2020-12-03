#%%
import wave
from recorder import Recorder
from pyaudio import paInt16
from analyser import Analyser
from matplotlib import pyplot

sample_rate = 44100
chunk_length = 2 #seconds
chunk_size = sample_rate * chunk_length

recorder = Recorder()

wf = wave.open('./recording.wav', 'rb')
chunk = wf.readframes(recorder.chunk_size)
wf.close()

chunk = recorder.read_chunk(2, chunk)

analyser = Analyser(recorder.sample_rate, recorder.chunk_length)

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
# %%
