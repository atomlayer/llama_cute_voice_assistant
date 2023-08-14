from time import sleep

import speech_recognition as sr
from oobabooga_api import generate
import pyttsx3
from silero_en import run_silero_en
from virtual_microphone import run_virtual_microphone


class llamaBot:
    """Voice chat bot based on Whisper and oobabooga"""

    def __init__(self):
        self.whisper_model_type = "base"

        self.voice_recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.tts_engine = pyttsx3.init()

    def run(self):
        """Run the listen-think-response loop"""
        input_words = self._voice_to_text()
        print("===> question:", input_words)
        if "miku" in input_words.lower() or "miko" in input_words.lower() \
                or "mikko" in input_words.lower():
            input_words = input_words[4:]
            answer = self.run_llm(input_words)
            print("==> answer:", answer)
            self._text_to_voice(answer)

    def _voice_to_text(self):
        """Listen voice and convert voice to text using OpenAI Whisper"""
        print("Listening...")
        with self.mic as source:
            self.voice_recognizer.adjust_for_ambient_noise(source)
            audio = self.voice_recognizer.listen(source)
            transcript = self.voice_recognizer.recognize_whisper(
                audio, self.whisper_model_type, language="en"
            )
            return transcript

    def run_llm(self, question):
        """Run model with input_data as input"""

        try:
            answer = generate(question)
        except:
            answer = "ERROR: Wrong Response"
        return answer

    max_silero_text_length = 140

    # to do: handle the situation when one word is 140 characters long
    def _split_text(self, answer):
        if len(answer) < self.max_silero_text_length:
            return [answer]

        text_array = answer.split(" ")

        current_text_array = []
        output_array = []
        for n in text_array:
            if len(" ".join(current_text_array + [n])) < self.max_silero_text_length:
                current_text_array.append(n)
            else:
                output_array.append(" ".join(current_text_array))
                current_text_array = []
                current_text_array.append(n)

        if len(current_text_array) > 0:
            output_array.append(" ".join(current_text_array))

        return output_array

    def _text_to_voice(self, answer):
        """Convert text to voice using TTS tools"""

        self.tts_engine.runAndWait()

        answer_array = self._split_text(answer)

        for n in answer_array:
            print("run_silero_en()")
            run_silero_en(n)

            print("run_virtual_microphone()")
            run_virtual_microphone()


if __name__ == "__main__":

    chat_bot = llamaBot()
    while True:
        chat_bot.run()
