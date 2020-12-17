from numpy import empty

def read_chunk(unit_size, raw_chunk): # unit size in bytes
        if len(raw_chunk) % unit_size != 0:
            raise ValueError(f'unit size {unit_size} and payload length {len(raw_chunk)} are incompatible')
        
        frame_length = len(raw_chunk) // unit_size
        frames = empty((frame_length,))
        for i in range(0, len(raw_chunk), unit_size):
            frame = int.from_bytes(raw_chunk[i:i+unit_size], 'little')
            frames[i // unit_size] = frame
        return frames