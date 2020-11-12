from os.path import dirname, realpath
from librosa.beat import plp
import pyaudio
import wave

FORMAT   = pyaudio.paInt16
CHANNELS = 2
RATE     = 44100
CHUNK    = 2 # seconds
DURATION = 4 # seconds
OUTPUT   = 'recording.wav'

chunk_size = CHUNK * RATE
chunks = int(RATE / chunk_size * DURATION)

pa = pyaudio.PyAudio()
stream = pa.open(
    rate=RATE, 
    channels=CHANNELS, 
    format=FORMAT,
    input=True,
    frames_per_buffer=CHUNK)
frames = []

print('* recording *')

try:
    for i in range(0, chunks):
        frame = stream.read(chunk_size)
        frames.append(frame)
except KeyboardInterrupt:
    pass

print('<> done recording <>')

stream.stop_stream()
stream.close()
pa.terminate()

dir_path = dirname(realpath(__file__))

wf = wave.open(OUTPUT, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(pa.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()