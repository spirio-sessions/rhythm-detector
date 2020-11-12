# __window_size__ = 2 # seconds

import pyaudio
import wave
import time

wave_read = wave.open('/Users/xmaek/Music/Music/Media.localized/Unknown Artist/Unknown Album/Sax_1.wav', 'rb')
py_audio  = pyaudio.PyAudio()

format    = py_audio.get_format_from_width(wave_read.getsampwidth())
channels  = wave_read.getnchannels()
framerate = wave_read.getframerate()

def callback(in_data, frame_count, time_info, status):
    frames = wave_read.readframes(frame_count)
    return (frames, pyaudio.paContinue)

stream = py_audio.open(
    format=format,
    channels=channels,
    rate=framerate,
    output=True,
    stream_callback=callback)

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wave_read.close()

py_audio.terminate()