from utils.files import create_data
from utils.files import read_file
from utils.output import show_data
from utils.output import playback_data
from utils.devices import get_sound_devices
from config import CORPUS_PATH, DATA_PATH

def main():
    create_data(CORPUS_PATH, DATA_PATH)
    playback_data(read_file("corpus/Natural/wav/01_MAD_1.wav"))

if __name__ == "__main__":
    main()
