from numpy import mean

from pythonosc.udp_client import SimpleUDPClient

class Analyser:

    def __init__(self, sample_rate, chunk_length, window_length=0.05, dominant_scale=1.0, strength_window_length=0.05):
        self.sample_rate = sample_rate
        self.chunk_length = chunk_length
        self.chunk_size = int(sample_rate * chunk_length)
        self.window_length = window_length
        self.window_size = int(sample_rate * window_length)
        self.dominant_scale = dominant_scale
        self.strength_window_length = strength_window_length
        self.strength_window_size = int((sample_rate * strength_window_length) / self.window_size)

    def smooth(self, chunk):
        half_window_size = self.window_size // 2
        smooth_chunk = [None] * len(chunk)

        for i in range(half_window_size): # TODO: omit?
            smooth_chunk[i] = mean(chunk[:i + (half_window_size)])
            smooth_chunk[-(i + 1)] = mean(chunk[-(i + 1 + half_window_size)])

        for i in range(half_window_size, len(chunk) - half_window_size):
            smooth_chunk[i] = mean(chunk[i-half_window_size : i+half_window_size])

        return smooth_chunk

    def window(self, chunk):
        window_count = int(self.chunk_size // self.window_size)
        windowed_chunk = []
        
        for w in range(window_count):
            windowed = mean(chunk[w*self.window_size : (w+1)*self.window_size])
            windowed_chunk.append(windowed)
        
        return windowed_chunk

    def flanks(self, chunk):
        flanks = [0]
        for i in range(1, len(chunk)):
            flanks.append(chunk[i] - chunk[i-1])
        return flanks

    def dominant(self, flanks):
        avg_rising = mean(list(filter(lambda f: f > 0, flanks)))
        dominant_flanks = list(map(lambda f: 1 if f > self.dominant_scale * avg_rising else 0, flanks))
        return dominant_flanks

    def strength(self, windowed, dominants):
        strengths = []

        for i in range(len(dominants)):
            if dominants[i] == 1 and i >= self.strength_window_size:
                strengths.append(windowed[i] / mean(windowed[i-self.strength_window_size:i]))
        return strengths

    def analyse(self, chunk):
        smooth_chunk = self.smooth(chunk)
        windowed_chunk = self.window(smooth_chunk)
        flanks = self.flanks(windowed_chunk)
        dominant_flanks = self.dominant(flanks)

        strengths = self.strength(windowed_chunk, dominant_flanks)
        
        beats = []
        for i in range(len(dominant_flanks)):
            if dominant_flanks[i] == 1:
                timestamp = i * (self.chunk_length / len(dominant_flanks))
                beats.append(timestamp)

        return (beats, strengths)