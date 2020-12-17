import wave

from util import read_chunk

class Loader:

    def __init__(self, file_path, chunk_length):
        self.file_path = file_path
        self.chunk_length = chunk_length
        self.handle = lambda _: print('no callback specified ...')

    def with_handle(self, callback):
        self.handle = callback
        return self

    def run(self):
        with wave.open(self.file_path, 'rb') as wf:
            frame_rate = wf.getframerate()
            chunk_size = int(self.chunk_length * frame_rate)
            unit_size  = wf.getsampwidth()

            print('beat detector is processing wav file..')

            raw_chunk = wf.readframes(chunk_size)

            while raw_chunk != b'':
                chunk = read_chunk(unit_size, raw_chunk)
                self.handle(chunk)
                raw_chunk = wf.readframes(chunk_size)

            print('beat detector processed wav')

            