import os

import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment, playback

from .constants import WAV_TYPE, MP3_TYPE, EN_LANGUAGE_CODE


class TextToAudio:

    old_sound_name = lambda self: '{}.{}'.format(self.name, MP3_TYPE)

    def __init__(self, text: str, name: str) -> None:
        self.text = text
        self.name = name

    def text_to_audio(self, lang: str=EN_LANGUAGE_CODE) -> None:
        sound_from_text = gTTS(self.text, lang=lang)
        sound_from_text.save(self.old_sound_name())

    def convert_type(self, format_: str=WAV_TYPE) -> None:
        self.sound = AudioSegment.from_mp3(self.old_sound_name())
        new_sound_name = '{}.{}'.format(self.name, format_)
        self.sound.export(new_sound_name, format=format_)

    def play(self):
        playback.play(self.sound)

    def run(self):
        self.text_to_audio()
        self.convert_type()
        self.play()



txt = input()



r = sr.Recognizer()
check = sr.AudioFile('hello.wav')
with check as source:
    data = r.record(source)
res = r.recognize_google(data)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print()
print(f"{bcolors.OKGREEN}{res}{bcolors.ENDC}")
print()
