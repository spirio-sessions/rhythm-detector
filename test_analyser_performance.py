# %%
from time import time
from loader import Loader
from analyser import Analyser, get_analyser_config

file_path = '/Users/xmaek/Music/Music/Media.localized/Unknown Artist/Unknown Album/Sax_1.wav'
chunk_length = 10.0
turns = 1

loader = Loader(file_path)
raw_signal = loader.load(chunk_length=chunk_length)

analyser_config = get_analyser_config('analyser_config.ini', 'Default')
analyser = Analyser(loader.get_sample_rate(), analyser_config=analyser_config)

start = time()
for _ in range(turns):
    analyser.peaks_to_timestamps(analyser.peak_pick(analyser.detect(analyser.smooth(raw_signal))))
end = time()
avg = (end - start) / turns

print('naive: %fs at %d turns' % (avg, turns))

start = time()
for _ in range(turns):
    analyser.analyse(raw_signal)
end = time()
avg = (end - start) / turns

print('optimised: %fs at %d turns' % (avg, turns))

# %%
