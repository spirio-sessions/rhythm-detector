from librosa.beat import plp
# import pythonosc

class Processor:

    def __init__(self, url, channels, sample_rate, chunk_length):
        # initialise osc client
        pass

    def detect(self, chunk):
        beats = None
        return beats

    def generate_osc(self, beats):
        osc = None
        return osc

    def process(self, chunk):
        beats = self.detect(chunk)
        osc = self.generate_osc(beats)
        # send osc