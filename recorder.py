import wave

from numpy import empty
from pyaudio import PyAudio, paInt16
from threading import Thread

from util import read_chunk

class Recorder:
    
    def __init__(self, channels=2, sample_rate=44100, chunk_length=2.0, enable_logging=True):
        self.channels = channels
        self.sample_rate = sample_rate
        self.chunk_length = chunk_length
        self.chunk_size = int(chunk_length * sample_rate)
        self.pa = PyAudio()
        self.enable_logging = enable_logging
        self.handle = lambda _: print('no callback specified ...') if enable_logging else None

    def log(self):
        if self.enable_logging:
            print(f'recorder received chunk of {self.chunk_size} frames ...')

    def with_handle(self, callback):
        self.handle = callback
        return self

    def record_chunk(self):
        chunk = self.pa.open(
            rate=self.sample_rate,
            channels=self.channels,
            format=paInt16,
            input=True
        ).read(self.chunk_size, False)
        
        wf = wave.open('./recording.wav', 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.pa.get_sample_size(paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(chunk)
        wf.close()

    def run(self):
        try:
            self.stream = self.pa.open(
                rate=self.sample_rate, 
                channels=self.channels,
                format=paInt16,
                input=True,
                frames_per_buffer=1024)

            print('beat detector is recording..')

            while True:
                raw_chunk = self.stream.read(self.chunk_size, False)
                # format is Int16 but since PyAudio internally uses half-bytes as blocks, we need to double the unit_size
                chunk = read_chunk(4, raw_chunk)
                Thread(target=self.handle, args=(chunk,)).start()
                
        except KeyboardInterrupt:
            print('beat detector stops recording - good bye')
            self.stream.stop_stream()
            self.stream.close()
            self.pa.terminate()