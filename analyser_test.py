#%%
from matplotlib import pyplot

from loader import Loader
from analyser import Analyser

loader = Loader('/Users/xmaek/Music/Music/Media.localized/Unknown Artist/Unknown Album/Sax_1.wav', 0)
signal = loader.load(chunk_length=5.0)
# loader = Loader('./recording.wav', 0)
# signal = loader.load(chunk_length=2.0)

# timestamps_raw = [ i/loader.get_sample_rate() for i in range(len(signal)) ]
# pyplot.figure(figsize=(20,5))
# pyplot.plot(timestamps_raw, signal, '.')
# pyplot.show()

analyser = Analyser(sample_rate=loader.get_sample_rate(), chunk_length=2.0)

smoothed_signal = analyser.smooth(signal)
detection_signal = analyser.detect(smoothed_signal)
peak_signal = analyser.peak_pick(detection_signal)

timestamps = [ i*analyser.hop_length for i in range(len(smoothed_signal))]

pyplot.figure(figsize=(20,5))
pyplot.plot(timestamps, smoothed_signal)
pyplot.ylim(2.5e8, 6.0e8)
# pyplot.show()

# pyplot.figure(figsize=(20,5))
# pyplot.plot(timestamps, detection_signal)
# pyplot.ylim(-0.5e8, 0.5e8)
# pyplot.show()

# pyplot.figure(figsize=(20,5))
# pyplot.plot(timestamps, peak_signal, 'hr')
# pyplot.ylim(0.5, 1.5)
# pyplot.show()

beats = analyser.peaks_to_timestamps(peak_signal)
for timestamp, _ in beats:
    pyplot.axvline(x=timestamp, color='r')
pyplot.show()

#%%