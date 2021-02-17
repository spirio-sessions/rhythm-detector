# %% imports

from matplotlib import pyplot
from loader import Loader
from analyser import Analyser, get_analyser_config

# %% step-wise analysis

file_path = '/Users/xmaek/Music/Music/Media.localized/Unknown Artist/Unknown Album/Sax_1.wav'
chunk_length = 10.0

loader = Loader(file_path)

analyser_config = get_analyser_config('analyser_config.ini', 'Default')
analyser = Analyser(loader.get_sample_rate(), analyser_config=analyser_config)

raw_signal = loader.load(chunk_length=chunk_length)
timestamps_raw = [ i/loader.get_sample_rate() for i in range(len(raw_signal)) ]
smoothed_signal = analyser.smooth(raw_signal)
detection_signal = analyser.detect(smoothed_signal)
peak_signal = analyser.peak_pick(detection_signal)
peak_timestamps = analyser.peaks_to_timestamps(peak_signal)

timestamps = [ i*analyser.hop_length for i in range(len(smoothed_signal))]

# %% plot analysis steps

figsize = (20,5)

pyplot.figure(figsize=figsize)
pyplot.plot(timestamps_raw, raw_signal, '.')
pyplot.yticks(ticks=[])
pyplot.xlabel('time [seconds]')
pyplot.show()

pyplot.figure(figsize=figsize)
pyplot.plot(timestamps, smoothed_signal)
pyplot.ylim(2.5e8, 6.0e8)
pyplot.yticks(ticks=[])
pyplot.xlabel('time [seconds]')
pyplot.show()

pyplot.figure(figsize=figsize)
pyplot.plot(timestamps, detection_signal)
pyplot.ylim(-0.75e8, 0.75e8)
pyplot.yticks(ticks=[])
pyplot.xlabel('time [seconds]')
pyplot.show()

pyplot.figure(figsize=figsize)
peak_signal_0_1 = list(map(lambda p: 1.0 if p > 0.0 else 0.0, peak_signal))
pyplot.plot(timestamps, peak_signal_0_1, 'hr')
pyplot.ylim(0.5, 1.5)
pyplot.yticks(ticks=[])
pyplot.xlabel('time [seconds]')
pyplot.show()

# %% plot beats over raw signal

figsize = figsize

pyplot.figure(figsize=figsize)
pyplot.plot(timestamps_raw, raw_signal, '.')
for timestamp, _ in peak_timestamps:
    pyplot.axvline(x=timestamp, color='r')
pyplot.yticks(ticks=[])
pyplot.xlabel('time [seconds]')
pyplot.show()

# %%