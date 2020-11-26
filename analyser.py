from numpy import mean

from pythonosc.udp_client import SimpleUDPClient

class Analyser:

    def __init__(self, sample_rate, chunk_length):
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
        window_count = int(self.chunk_size // window_size)
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

    def analyse(self, chunk):
        smooth_chunk = self.smooth(chunk, 1/16) # scale to 1/32 beat at 120 bpm
        windowed_chunk = self.window(smooth_chunk)
        flanks = self.flanks(windowed_chunk)
        dominant_flanks = self.dominant(flanks)
        
        beats = []
        for i in range(len(dominant_flanks)):
            if dominant_flanks[i] == 1:
                timestamp = i * (self.chunk_length / len(dominant_flanks))
                beats.append(timestamp)

        return beats