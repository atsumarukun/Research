from typing import TypedDict
from numpy import ndarray

class File(TypedDict):
    path: str
    channels: int
    width: int
    framerate: int
    data: ndarray
