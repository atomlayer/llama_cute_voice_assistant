#! python3.11

import warnings

warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")
warnings.filterwarnings("ignore", message=".*Using cache found in.*")
warnings.filterwarnings("ignore", message=".*loaded more than 1 DLL from.*")
warnings.filterwarnings("ignore", message=".*RNN module weights are not part of single contiguous chunk of memory.*")

from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import argparse
import io
import os
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
from sys import platform

import settings
from oobabooga_api import generate
from silero_en import SileroModel
from split_text_manager import split_text
from virtual_microphone import run_virtual_microphone
import re
import logging

logging.getLogger("tensorflow").setLevel(logging.ERROR)


def main():
    parser = argparse.ArgumentParser()

    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args()

    # The last time a recording was retreived from the queue.
    phrase_time = None
    # Current raw audio bytes.
    last_sample = bytes()
    # Thread safe Queue for passing data from the threaded recording callback.
    data_queue = Queue()
    # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
    recorder = sr.Recognizer()
    recorder.energy_threshold = settings.energy_threshold
    # Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
    recorder.dynamic_energy_threshold = False

    # Important for linux users.
    # Prevents permanent application hang and crash by using the wrong Microphone
    if 'linux' in platform:
        mic_name = args.default_microphone
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")
            return
        else:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    source = sr.Microphone(sample_rate=16000, device_index=index)
                    break
    else:
        source = sr.Microphone(sample_rate=16000)

    # Flush stdout.
    print('', end='', flush=True)

    print("Whisper model is loading...")

    # Load / Download model
    model = settings.whisper_model
    if settings.whisper_model != "large" and not settings.non_english:
        model = model + ".en"
    audio_model = whisper.load_model(model)

    record_timeout = settings.record_timeout
    phrase_timeout = settings.phrase_timeout

    temp_file = NamedTemporaryFile().name
    transcription = []

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:
        """
        Threaded callback function to recieve audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        data = audio.get_raw_data()
        data_queue.put(data)

    # Create a background thread that will pass us raw audio bytes.
    # We could do this manually but SpeechRecognizer provides a nice helper.
    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    # Cue the user that we're ready to go.
    print("Whisper model loaded.")

    print("Silero model is loading...")
    silero_model = SileroModel()
    silero_model.load_model()
    print("Silero model loaded.\n")

    def get_wake_word(input_words):
        for n in settings.wake_words:
            if n.lower() in input_words.lower():
                return n

    def clear_input_text(text, wake_word):
        text_input = text[len(wake_word):]
        try:
            text_input = re.sub(r'^,\s', '', text_input)
            text_input = text_input[0].capitalize() + text_input[1:]
            return text_input
        except:
            return text_input

    def text_to_voice(answer):
        """Convert text to voice using TTS tools"""

        answer_array = split_text(answer)

        for n in answer_array:
            silero_model.run_silero_en(n)
            run_virtual_microphone()

    def run_llm(question):
        """Run model with input_data as input"""

        try:
            answer = generate(question)
        except:
            answer = "ERROR: Wrong Response"
        return answer

    def console_write(text_data=None):
        # Clear the console to reprint the updated transcription.
        os.system('cls' if os.name == 'nt' else 'clear')
        for line in transcription:
            print(line)

        if text_data:
            print("\n--> " + text_data)

        # Flush stdout.
        print('', end='', flush=True)

    is_first = True

    while True:
        try:
            now = datetime.utcnow()
            # Pull raw recorded audio from the queue.
            if not data_queue.empty():
                phrase_complete = False

                # If enough time has passed between recordings, consider the phrase complete.
                # Clear the current working audio buffer to start over with the new data.
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    last_sample = bytes()
                    phrase_complete = True

                # This is the last time we received new audio data from the queue.
                phrase_time = now

                # Concatenate our current audio data with the latest audio data.
                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data

                # Use AudioData to convert the raw data to wav data.
                audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                wav_data = io.BytesIO(audio_data.get_wav_data())

                # Write wav data to the temporary file as bytes.
                with open(temp_file, 'w+b') as f:
                    f.write(wav_data.read())

                # Read the transcription.
                result = audio_model.transcribe(temp_file, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                wake_word = get_wake_word(text)

                # If we detected a pause between recordings, add a new item to our transcripion.
                # Otherwise edit the existing one.
                if phrase_complete or is_first:
                    is_first = False
                    if wake_word:
                        input_words = clear_input_text(text, wake_word)
                        transcription.append("You: " + input_words)

                        answer = run_llm(input_words)
                        transcription.append(f"{settings.oobabooga_api_name}: " + answer)
                        console_write()
                        text_to_voice(answer)

                console_write(text_data=text)

                sleep(0.25)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()
