from fileinput import close
import speech_recognition as sr
import pyttsx3
# from aiy.board import Board, Led

r = sr.Recognizer()
engine = pyttsx3.init()

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

def inicializarEngine():
    voices = engine.getProperty('voices')
    # for voice in voices:
    #     print(voice)

    #EN EL RASPI
    # engine.setProperty('voice', voices[20].id)

    #EN WINDOWS DEPENDE DE LA INSTALACION
    engine.setProperty('voice', voices[2].id)
    
    engine.setProperty('rate', 140)

def raspiHabla(text):
    engine.say(text)
    engine.runAndWait()


def main():
    inicializarEngine()
    raspiHabla("Bienvenido Señor Usuario")
    raspiHabla("Por favor seleccione una de las siguientes opciones")
    

if __name__ == "__main__":
    main()