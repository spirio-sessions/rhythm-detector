import wave
from concurrent.futures import ThreadPoolExecutor
from os import _exit, EX_OK

from numpy import empty
from pyaudio import PyAudio, paInt16

from util import read_chunk

class Recorder:
    
    def __init__(self, device_number=0, chunk_length=2.0, enable_logging=True):
        self.device_number = device_number
        self.pa = PyAudio()
        self.channels = int(self.pa.get_device_info_by_index(device_number)['maxInputChannels'])
        self.sample_rate = int(self.pa.get_device_info_by_index(device_number)['defaultSampleRate'])
        self.chunk_length = chunk_length
        self.chunk_size = int(chunk_length * self.sample_rate)
        self.enable_logging = enable_logging
        self.handle = lambda _: print('no callback specified ...') if enable_logging else None

    def log(self):
        if self.enable_logging:
            print(f'recorder received chunk of {self.chunk_size} frames ...')

    def with_handle(self, callback):
        self.handle = callback
        return self

    def on_raw_chunk_recorded(self, raw_chunk):
        unit_size = self.pa.get_sample_size(paInt16)
        chunk = read_chunk(unit_size, self.channels, raw_chunk)
        self.handle(chunk)

    def get_sample_rate(self, device_number=None):
        if device_number == None:
            device_number = self.device_number
        
        return int(self.pa.get_device_info_by_index(device_number)['defaultSampleRate'])

    def get_max_channels(self, device_number=None):
        if device_number == None:
            device_number = self.device_number

        return int(self.pa.get_device_info_by_index(device_number)['maxInputChannels'])

    def record_chunk(self, device_number=None):
        if device_number == None:
            device_number = self.device_number

        chunk = self.pa.open(
            input_device_index=device_number,
            rate=self.get_sample_rate(device_number),
            channels=self.get_max_channels(device_number),
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
        self.stream = self.pa.open(
            input_device_index=self.device_number,
            rate=self.sample_rate, 
            channels=self.channels,
            format=paInt16,
            input=True,
            frames_per_buffer=1024)

        executor = ThreadPoolExecutor(max_workers=2)
        print('beat detector is recording..')
        running = True
        while running:
            try:
                raw_chunk = self.stream.read(self.chunk_size, False)
                future = executor.submit(self.on_raw_chunk_recorded, raw_chunk)
            except KeyboardInterrupt:
                running = False
                future.cancel()

        executor.shutdown(wait=False)

        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()
        
        print()
        print('beat detector stopped recording - good bye')

        _exit(EX_OK)