import wave
import pyaudio
import numpy as np

OUTPUT_DEVICE_NAME = "HD-Audio Generic: ALC285 Analog (hw:1,0)"

with wave.open("./corpus/Natural/wav/01_MAD_1.wav", "r") as f:
    stream = f.readframes(f.getnframes())
    channels = f.getnchannels()
    sample_size = f.getsampwidth()
    sample_rate = f.getframerate()

if sample_size == 1:
    dtype = "int8"
    format=pyaudio.paInt8
elif sample_size == 2:
    dtype = "int16"
    format=pyaudio.paInt16
elif sample_size == 3:
    dtype = "int24"
    format=pyaudio.paInt24
elif sample_size == 4:
    dtype = "int32"
    format=pyaudio.paInt32

data = np.frombuffer(stream, dtype=dtype)

p = pyaudio.PyAudio()
output_device_index: int
for i in range(p.get_device_count()):
    device = p.get_device_info_by_index(i)
    if device["name"] == OUTPUT_DEVICE_NAME:
        output_device_index = int(device["index"])
        break

stream = p.open(format=format,
                channels=channels,
                rate=sample_rate,
                frames_per_buffer=1024,
                output_device_index=0,
                output=True)

stream.write(data)
stream.close()