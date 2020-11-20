from pyaudio import PyAudio, paInt16
from numpy import empty

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

    def read_chunk(self, unit_size, chunk):
        if len(chunk) % unit_size != 0:
            raise ValueError(f'unit size {unit_size} and payload length {len(chunk)} are incompatible')
        
        frame_length = len(chunk) // unit_size
        frames = empty((frame_length,))
        for i in range(0, len(chunk), unit_size):
            frame = int.from_bytes(chunk[i:i+unit_size], 'little')
            frames[i // unit_size] = frame
        return frames

    def run(self):
        try:
            self.stream = self.pa.open(
                rate=self.sample_rate, 
                channels=self.channels,
                format=paInt16,
                input=True,
                frames_per_buffer=1024)

            while True:
                raw_chunk = self.stream.read(self.chunk_size, False)
                chunk = self.read_chunk(2, raw_chunk)
                self.log()
                self.handle(chunk)
        except KeyboardInterrupt:
            self.stream.stop_stream()
            self.stream.close()
            self.pa.terminate()