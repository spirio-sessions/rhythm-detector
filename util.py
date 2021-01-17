from numpy import empty, max, min

def read_chunk(unit_size, channels, raw_chunk, channel_index=0): # unit size in bytes
    # one frame is sent from each channel repsectively and queued in sequence
    frame_size = unit_size * channels # frame size in bytes
    if len(raw_chunk) % frame_size != 0:
        raise ValueError(f'unit size {unit_size} with {channels} channels and payload length {len(raw_chunk)} are incompatible')
    
    frame_count = len(raw_chunk) // frame_size
    chunk = empty((frame_count,))
    for i in range(0, len(raw_chunk), frame_size):
        frame = int.from_bytes(raw_chunk[i+unit_size*channel_index : i+unit_size*(channel_index+1)], 'little')
        chunk[i // frame_size] = frame

    half_amp = (max(chunk) - min(chunk)) // 2
    chunk = chunk - half_amp

    return chunk