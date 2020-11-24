from pythonosc.udp_client import SimpleUDPClient

from time import sleep
from numpy import concatenate, mean, sin, abs
from matplotlib import pyplot
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

    def smooth(self, chunk, window_length=0.05): # window length in seconds
        window_size = int(self.sample_rate * window_length)
        half_window_size = window_size // 2
        smooth_chunk = [None] * len(chunk)

        for i in range(half_window_size):
            smooth_chunk[i] = mean(chunk[:i + (half_window_size)])
            smooth_chunk[-(i + 1)] = mean(chunk[-(i + 1 + (half_window_size))])

        for i in range(half_window_size, len(chunk) - half_window_size):
            smooth_chunk[i] = mean(chunk[i-half_window_size : i+half_window_size])

        return smooth_chunk

    def window(self, chunk, window_length=0.05): # window length in seconds
        window_size = int(self.sample_rate * window_length)
        window_count = self.chunk_size // window_size
        windowed_chunk = []
        
        for w in range(window_count):
            windowed = mean(chunk[w*window_size : (w+1)*window_size])
            windowed_chunk.append(windowed)
        
        return windowed_chunk

    def flanks(self, chunk):
        flanks = [0]
        for i in range(1, len(chunk)):
            flanks.append(chunk[i] - chunk[i-1])
        return flanks

    def dominant(self, flanks, scale=1.0):
        avg_rising = mean(list(filter(lambda f: f > 0, flanks)))
        dominant_flanks = list(map(lambda f: 1 if f > scale * avg_rising else 0, flanks))
        return dominant_flanks

    def generate_osc(self, beats):
        timestamps = []
        for i in range(len(beats)):
            if beats[i] == 1:
                timestamp = i * (self.chunk_length / len(beats))
                timestamps.append(timestamp)

        return ('/generate/pulse', timestamps)

    def process(self, chunk):
        smooth_chunk = self.smooth(chunk, 1/16) # scale to 1/32 beat at 120 bpm
        windowed_chunk = self.window(smooth_chunk)
        flanks = self.flanks(windowed_chunk)
        dominant_flanks = self.dominant(flanks)
        path, beats = self.generate_osc(dominant_flanks)

        Thread(target=ticks(beats)).start()
        f = open('./out', mode='w', encoding='utf-8')
        f.write(path + ' ' + str(beats))
        f.close()
        # self.osc_client.send_message(path, beats)

chunk = [abs(2000 * sin(x * 8*3.1415/88200)) for x in range(88200)]
p = Processor(('127.0.0.1', 5050), 2, 44100, 2)
p.process(chunk)