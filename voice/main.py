from pygame import mixer, _sdl2 as devices
import speech_recognition as sr
import pyttsx3 as tts
import time
import os


class Maxim():
    def __init__(self):
        print('Program start')

        self.language = ['ru-RU', 'en-EN']
        self.audio_name = 'audio.wav'
        
        print('Start settings')
        self.var = sr.Recognizer()
        self.mic = sr.Microphone()
        self.engine = tts.init()
        self.voices = self.engine.getProperty('voices')

        i = 1
        for voice in self.voices:
            print(f'{i} - {voice.name}')
            i += 1

        inp = int(input('Input engine -> '))
        self.engine.setProperty('voice', self.voices[inp - 1].id)

        self.engine.setProperty("rate", 120)
        self.engine.setProperty("volume", 0.8)

        mixer.init()
        self.dev = devices.audio.get_audio_device_names(False)
        
        i = 1
        for dev in self.dev:
            print(f'{i} - {dev}')
            i += 1

        mixer.quit()

        inp = int(input('Input device -> '))
        self.device = self.dev[inp - 1]

        i = 1
        for l in self.language:
            print(f'{i} - {l}')
            i += 1
        
        inp = int(input('Input language -> '))
        self.lang = self.language[inp - 1]

        print('Setting setup complete')

    def _record(self):
        with self.mic as mic:
            self.var.adjust_for_ambient_noise(mic)
            print('Rec*')
            audio = self.var.listen(mic)
            try:
                print(f'{(text_out := self.var.recognize_google(audio, language=self.lang, pfilter=0))}')
                return text_out
            except: pass

    def save_audio(self):
        s = self.engine
        text = self._record()
        if text:
            s.save_to_file(text, self.audio_name)
            s.runAndWait()
            print('file saved')

    def load_audio(self):
        try:
            mixer.music.load(self.audio_name)
            mixer.music.play()
        except:
            print('Error')



if __name__ == '__main__':
    bot = Maxim()

    while True:
        bot.save_audio()
        time.sleep(1)
        mixer.init(devicename=bot.device)
        if mixer.music.get_busy() == False:
            bot.load_audio()
        while os.path.isfile(bot.audio_name):
            if mixer.music.get_busy() == False:
                try:
                    mixer.quit()
                    os.remove(bot.audio_name)
                except Exception as e:
                    print(e)
