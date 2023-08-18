# from pygame import mixer, _sdl2 as devicer

# mixer.init() # Initialize the mixer, this will allow the next command to work
#
# # Returns playback devices, Boolean value determines whether they are Input or Output devices.
# print("Inputs:", devicer.audio.get_audio_device_names(True))
# print("Outputs:", devicer.audio.get_audio_device_names(False))
#
# mixer.quit() # Quit the mixer as it's initialized on your main playback device


import time
from pygame import mixer

import settings


def run_virtual_microphone():
    mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')  # Initialize it with the correct device
    mixer.music.load(settings.wave_file_name)  # Load the mp3
    mixer.music.play()  # Play it

    while mixer.music.get_busy():  # wait for music to finish playing
        time.sleep(0.1)
    mixer.quit()  # Quit the mixer as it's initialized on your main playback device
