import os

import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment, playback

from helpers import bcolors
from constants import WAV_TYPE, MP3_TYPE, EN_LANGUAGE_CODE, FILE_NAME


class TextToAudio:

    old_sound_name = lambda self: '{}.{}'.format(self.name, MP3_TYPE)

    def __init__(self, text: str, name: str) -> None:
        self.text = text
        self.name = name

    def text_to_audio(self, lang: str) -> None:
        sound_from_text = gTTS(self.text, lang=lang)
        sound_from_text.save(self.old_sound_name())

    def convert_type(self, format_: str) -> None:
        self.sound = AudioSegment.from_mp3(self.old_sound_name())
        new_sound_name = '{}.{}'.format(self.name, format_)
        self.sound.export(new_sound_name, format=format_)

    def play(self):
        playback.play(self.sound)

    def run(self, lang: str, format_: str):
        self.text_to_audio(lang)
        self.convert_type(format_)
        self.play()


class AudioToText:

    def __init__(self, name) -> None:
        self.name = name
        self.recognizer = sr.Recognizer()

    def get_audio_file(self, format_: str):
        sound_name =  '{}.{}'.format(self.name, format_)
        self.audio_file = sr.AudioFile(sound_name)

    def get_text_from_audio(self):
        with self.audio_file as source:
            data = self.recognizer.record(source)
        try:
            res = self.recognizer.recognize_google(data)
        except sr.UnknownValueError:
            err_message = 'can\'t read this text from palyed voice.'
            print(f"\n{bcolors.DANGER}{err_message}{bcolors.ENDC}", end='')
            res = ''
        return res

    def run(self, format_: str):
        self.get_audio_file(format_)
        result = self.get_text_from_audio()
        return result


class SoundsSpeach:

    def __init__(self) -> None:
        self.text = input(f'\n{bcolors.BLUE}Input a text: {bcolors.ENDC}')

    def handler(self):
        TextToAudio(self.text, FILE_NAME).run(EN_LANGUAGE_CODE, WAV_TYPE)
        result = AudioToText(FILE_NAME).run(WAV_TYPE)
        print(f"\n{bcolors.GREEN}{result}{bcolors.ENDC}", end='\n\n')

if __name__ == '__main__':
    SoundsSpeach().handler()
