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
from osc_sender import OscSender

sender = OscSender(('127.0.0.1', 9998))
sender.send([0.3, 0.8, 1.3, 1.8])
# %%
