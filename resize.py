import os
import wave
import numpy as np
from typing import Final

from type.filetype import File

from matplotlib import pyplot as plt

CORPUS_PATH = "corpus/Acted/wav"

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

def __create_dir(path: str) -> bool:
    if (not os.path.isdir(path)):
        if (path.rfind("/") == -1 or __create_dir(path[:path.rfind("/")])):
            os.mkdir(path)
        else:
            return False
    return True

def get_files(path: str, files=[]) -> list:
    for file_ in os.listdir(path):
        if os.path.isdir(f"{path}/{file_}"):
            get_files(f"{path}/{file_}", files)
        else:
            files.append(read_file(f"{path}/{file_}"))
    return files

def get_max_size(files: Final[File]) -> int:
    max_size = 0
    for file_ in files:
        max_size = max(max_size, len(file_["data"]))
    return max_size

def resize(file_: Final[File], size: int) -> Final[File]:
    file_["data"] = np.append(file_["data"], np.zeros(size - len(file_["data"]), "int16"))
    return file_

def write_files(file_: Final[File]):
    new_file = "data" + file_["path"][file_["path"].find("/"):]

    if (not os.path.isdir(new_file[:new_file.rfind("/")])):
        __create_dir(new_file[:new_file.rfind("/")])

    with wave.open(new_file, "wb") as f:
        f.setnchannels(file_["channels"])
        f.setsampwidth(file_["width"])
        f.setframerate(file_["framerate"])
        f.writeframes(file_["data"].tobytes())

def main():
    files = get_files(CORPUS_PATH)
    max_size = get_max_size(files)
    for file_ in files:
        write_files(resize(file_, max_size))

if __name__ == "__main__":
    main()
