from pyaudio import PyAudio, paInt16

class Recorder:
    
    def __init__(self, channels=2, sample_rate=44100, chunk_length=2.0, enable_logging=True):
        self.channels = channels
        self.sample_rate = sample_rate
        self.chunk_length = chunk_length
        self.chunk_size = int(chunk_length * sample_rate)
        self.pa = PyAudio()
        self.enable_logging = enable_logging
        self.handle = lambda : print('no callback specified ...') if enable_logging else None

    def log(self):
        if self.enable_logging:
            print(f'recorder received chunk of {self.chunk_size} frames ...')

    def with_handle(self, callback):
        self.handle = callback
        return self

    def run(self):
        try:
            self.stream = self.pa.open(
                rate=self.sample_rate, 
                channels=self.channels, 
                format=paInt16,
                input=True,
                frames_per_buffer=1024)

            while True:
                chunk = self.stream.read(self.chunk_size)
                self.log()
                self.handle(chunk)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(e)

        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()