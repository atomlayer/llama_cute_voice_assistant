# !pip install -q torchaudio omegaconf

import torch
from omegaconf import OmegaConf
from IPython.display import Audio, display
import soundfile as sf
import simpleaudio as sa

import settings

torch.hub.download_url_to_file('https://raw.githubusercontent.com/snakers4/silero-models/master/models.yml',
                               'latest_silero_models.yml',
                               progress=False)
models = OmegaConf.load('latest_silero_models.yml')



import torch

language = 'ru'
speaker = 'kseniya_v2'
# language = 'en'
# speaker = 'v3_en'
sample_rate = 16000
device = torch.device(settings.device)
model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=speaker)
model.to(device)  # gpu or cpu


audio = model.apply_tts(texts=["Привет. Все ли хорошо?"],
                        sample_rate=sample_rate)


print(example_text)
display(Audio(audio[0], rate=sample_rate))


from pydub import AudioSegment




sf.write(settings.wave_file_name, audio[0], sample_rate)


# from pydub import AudioSegment
#
# # Load audio file
# sound = AudioSegment.from_file('filename.wav')
#
# # Increase pitch by 2 semitones
# new_sound = sound +15
#
# # Export modified audio file
# new_sound.export('filename.wav', format="wav")



wave_obj = sa.WaveObject.from_wave_file('filename.wav')
play_obj = wave_obj.play()
play_obj.wait_done()