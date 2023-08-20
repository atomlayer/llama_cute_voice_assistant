import torch
import soundfile as sf
import settings


class SileroModel:

    def load_model(self):
        self.language = 'en'
        self.speaker = 'lj_16khz'
        self.device = torch.device(settings.device)

        self.model, self.symbols, \
            self.sample_rate, self.example_text, self.apply_tts = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                                                 model='silero_tts',
                                                                                 language=self.language,
                                                                                 speaker=self.speaker)
        self.model_device = self.model.to(self.device)  # gpu or cpu

    def run_silero_en(self, text):
        audio = self.apply_tts(texts=[text],
                               model=self.model_device,
                               sample_rate=self.sample_rate,
                               symbols=self.symbols,
                               device=self.device)

        sf.write(settings.wave_file_name, audio[0], self.sample_rate)
