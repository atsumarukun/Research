import pyaudio
import numpy as np
from typing import Final
from matplotlib import pyplot as plt

from type.filetype import File
from config import OUTPUT_DEVICE_NAME

def show_data(file_: Final[File]):
    plt.plot(file_["data"])
    plt.show()

def playback_data(file_: Final[File]):
    p = pyaudio.PyAudio()
    output_device_index: int
    for i in range(p.get_device_count()):
        device = p.get_device_info_by_index(i)
        if device["name"] == OUTPUT_DEVICE_NAME:
            output_device_index = int(device["index"])
            break

    stream = p.open(format=pyaudio.paInt16,
                    channels=file_["channels"],
                    rate=file_["framerate"],
                    output_device_index=output_device_index,
                    output=True)

    stream.write(file_["data"])
    stream.close()
