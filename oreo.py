from fileinput import close
import speech_recognition as sr
import gtts
from playsound import playsound
# import os
import pyttsx3
#from aiy.board import Board, Led


r = sr.Recognizer()

# def EncenderLed():
#     Board().led.state = Led.ON

# def ApagarLed():
#     try:
#         Board().led.state = Led.OFF
#     except(RuntimeError):
#         pass

# def EsperarClick():
#     Board().button.wait_for_press()

# def EsperarSoltar():
#     Board().button.wait_for_release()

with sr.Microphone() as source:
    # EncenderLed()
    # EsperarClick()
    # ApagarLed()
    print("Iniciando Grabación de Audio...")
    audio_data = r.record(source, duration=7)
    print("Reconociendo...")
    text = r.recognize_google(audio_data, language="es-ES")
    # EsperarSoltar()
    print(text)
    tts = gtts.gTTS(text, lang="es")
    # tts.save("pista.mp3")


    engine = pyttsx3.init()
    for voice in engine.getProperty('voices'):
        print(voice)
    # engine.say(text)
    # engine.runAndWait()
    
    
    # playsound("pista.mp3")
    