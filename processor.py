from librosa.beat import plp, beat_track
from pythonosc.udp_client import SimpleUDPClient

from time import sleep
from numpy import concatenate, abs, mean
from threading import Thread

def tick(t):
    sleep(t)
    print('\a')

def ticks(ts):
    ts = concatenate(([0.0], ts))
    def do_ticks():
        for i in range(len(ts) - 1):
            tick(ts[i+1] - ts[i])
    return do_ticks

class Processor:

    def __init__(self, target, channels, sample_rate, chunk_length):
        ip, port = target
        self.osc_client = SimpleUDPClient(ip, int(port))
        self.channels = channels
        self.sample_rate = sample_rate
        self.chunk_length = chunk_length
        self.chunk_size = sample_rate * chunk_length

    def window(self, chunk, window_lengt=0.05): # window length in seconds
        window_size = int(self.sample_rate * window_lengt)
        window_count = int(self.chunk_size) // window_size
        windowed = []
        for w in range(window_count):
            window = chunk[w*window_size : (w+1)*window_size]
            windowed.append(mean(window))
        return windowed

    def flanks(self, chunk):
        flanks = [0]
        for i in range(1, len(chunk)):
            flanks.append(chunk[i] - chunk[i-1])
        return flanks

    def detect(self, chunk):
        # chunk_size = int(self.sample_rate * self.chunk_length)
        # hop = int((4/7)*chunk_size)
        # win = int((3/7)*chunk_size)
        # beats = plp(chunk, sr=self.sample_rate) #hop_length=hop, win_length=win)

        #_, beats = beat_track(chunk, sr=self.sample_rate, units='time')
        windowed = self.window(chunk)
        beats = self.flanks(windowed)
        return beats

    def generate_osc(self, beats):
        return ('/generate/pulse', beats)

    def process(self, chunk):
        beats = self.detect(chunk)
        beats = list(map(str, beats))
        output = ' '.join(beats)
        file = open('./log', 'w')
        file.write(output)
        file.close()
        # path, value = self.generate_osc(beats)
        # Thread(target=ticks(beats)).start()
        # print(beats)
        # self.osc_client.send_message(path, value)