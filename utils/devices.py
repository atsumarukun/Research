import pyaudio

def get_sound_devices() -> list:
    p = pyaudio.PyAudio()
    devices = []
    for i in range(p.get_device_count()):
        devices.append(p.get_device_info_by_index(i))
    return devices
