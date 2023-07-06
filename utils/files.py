import os
import wave
import numpy as np
from typing import Final
from matplotlib import pyplot as plt

from type.filetype import File

def __create_dir(path: str) -> bool:
    if (not os.path.isdir(path)):
        if (path.rfind("/") == -1 or __create_dir(path[:path.rfind("/")])):
            os.mkdir(path)
        else:
            return False
    return True

def __get_max_size(files: list) -> int:
    return max(list(map(lambda v: len(v["data"]), files)))

def __resize(file_: Final[File], size: int) -> Final[File]:
    file_["data"] = np.append(file_["data"], np.zeros(size - len(file_["data"]), "int16"))
    return file_

def __write_file(file_: Final[File], path):
    write_file = f"{path}{file_['path'][file_['path'].find('/'):]}"

    if (not os.path.isdir(write_file[:write_file.rfind("/")])):
        __create_dir(write_file[:write_file.rfind("/")])

    with wave.open(write_file, "wb") as f:
        f.setnchannels(file_["channels"])
        f.setsampwidth(file_["width"])
        f.setframerate(file_["framerate"])
        f.writeframes(file_["data"].tobytes())

def read_file(path: str) -> Final[File]:
    with wave.open(path, "rb") as f:
        stream = f.readframes(f.getnframes())
        file_ = File({
            "path": path,
            "channels": f.getnchannels(),
            "width": f.getsampwidth(),
            "framerate": f.getframerate(),
            "data": np.frombuffer(stream, "int16")
        })
    return file_

def read_files(path: str, files=[]) -> list:
    for file_ in os.listdir(path):
        if os.path.isdir(f"{path}/{file_}"):
            read_files(f"{path}/{file_}", files)
        else:
            files.append(read_file(f"{path}/{file_}"))
    return files

def create_data(input_path, output_path):
    files = read_files(input_path)
    max_size = __get_max_size(files)
    for file_ in files:
        __write_file(__resize(file_, max_size), output_path)
