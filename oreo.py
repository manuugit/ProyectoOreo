from fileinput import close
import speech_recognition as sr
import pyttsx3
from aiy.board import Board, Led


r = sr.Recognizer()

def EncenderLed():
    Board().led.state = Led.ON

def ApagarLed():
    try:
        Board().led.state = Led.OFF
    except(RuntimeError):
        pass

def EsperarClick():
    Board().button.wait_for_press()

def EsperarSoltar():
    Board().button.wait_for_release()

with sr.Microphone() as source:
    EncenderLed()
    EsperarClick()
    ApagarLed()
    print("Iniciando Grabación de Audio...")
    audio_data = r.record(source, duration=7)
    print("Reconociendo...")
    text = r.recognize_google(audio_data, language="es-ES")
    EsperarSoltar()
    print(text)

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[20].id)
    engine.setProperty('rate', 140)
    engine.say(text)
    engine.runAndWait()
    
    
    #playsound("pista.mp3")
    