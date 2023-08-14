# pip install -q torchaudio omegaconf

import torch
import soundfile as sf
import simpleaudio as sa

import settings


def run_silero_en(text):

    language = 'en'
    speaker = 'lj_16khz'
    device = torch.device(settings.device)
    model, symbols, sample_rate, example_text, apply_tts = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                          model='silero_tts',
                                                                          language=language,
                                                                          speaker=speaker)
    model = model.to(device)  # gpu or cpu
    audio = apply_tts(texts=[text],
                      model=model,
                      sample_rate=sample_rate,
                      symbols=symbols,
                      device=device)


    sf.write(settings.wave_file_name, audio[0], sample_rate)


# wave_obj = sa.WaveObject.from_wave_file('filename.wav')
# play_obj = wave_obj.play()
# play_obj.wait_done()
