import wave

from numpy import empty
from util import read_chunk

class Loader:

    def __init__(self, file_path, chunk_length):
        self.file_path = file_path
        self.chunk_length = chunk_length
        self.handle = lambda _: print('no callback specified ...')

    def with_handle(self, callback):
        self.handle = callback
        return self

    def load(self, file_path=None, chunk_length=None):
        if file_path == None:
            file_path = self.file_path

        with wave.open(file_path, 'rb') as wf:
            
            if chunk_length == None: # read all
                raw_chunk = wf.readframes(1024)
                raw_chunks = [raw_chunk]

                while raw_chunk != b'':
                    raw_chunk = wf.readframes(1024)
                    raw_chunks.append(raw_chunk)

                data = b''.join(raw_chunks)
                unit_size  = wf.getsampwidth()
                return read_chunk(unit_size, data)

            else: # read specified chunk
                frame_rate = wf.getframerate()
                chunk_size = int(chunk_length * frame_rate)
                unit_size  = wf.getsampwidth()
                raw_chunk = wf.readframes(chunk_size)
                return read_chunk(unit_size, raw_chunk)

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

            