from tokenize import String
import speech_recognition as sr
import pyttsx3
# from aiy.board import Board, Led

r = sr.Recognizer()
engine = pyttsx3.init()
Diccionario_sentimientos = {'Confundido':'Confusion',
    'Vacio':'Hipotimia',
    'Solo':'Hipotimia',
    'Estresado':'Estres',
    'Angustiado':'Hipotimia',
    'Euforico':'Euforia',
    'Ansioso':'Ansiedad',
    'Tranquilo':'Tranquilidad',
    'Emocionado':'Energico',
    'Asustado':'Ansiedad',
    'Decepcionado':'Hipotimia',
    'Desesperado':'Ansiedad',
    'Energico':'Energico',
    'Cansado':'Cansancio',
    'Agotado':'Cansancio',
    'Animado':'Euforia',
    'Motivado':'Euforia',
    'Desmotivado':'Hipotimia',
    'Aburrido':'Hipotimia',
    'Melancólico':'Hipotimia',
    'Humillado':'Hipotimia',
    'Frustrado':'Depresion',
    'Enojado':'Enojo',
    'Abrumado':'Hipotimia',
    'Envidioso':'Envidioso',
    'Orgulloso':'Orgulloso',
    'Decaido':'Decaido'}

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
    print(text)
    engine.say(text)
    engine.runAndWait()

def reconocerVoz(seconds) -> String:
    text = "Trying"
    with sr.Microphone() as source:
        # EncenderLed()
        # EsperarClick()
        # ApagarLed()
        print("Iniciando Grabación de Audio...")
        audio_data = r.record(source, duration=seconds)
        print("Reconociendo...")
        text = r.recognize_google(audio_data, language="es-ES")
        # EsperarSoltar()
    return text



def getKeyWords(text,array): #Texto de usuario, Array de posibles respuestas
    retArray = []
    text = text.upper()
    print(text)
    for palabra in array:
        palabre = palabra[:len(palabra)-1]+'a'
        # palabre[len(palabre)-1] = 'a'
        if text.__contains__(palabra.upper()):
            retArray.append(palabra)
        if text.__contains__(palabre.upper()):
            retArray.append(palabre)
    if retArray == []:
        return "No hay elementos"        
    return retArray


def main():
    inicializarEngine()
    while True:
        raspiHabla("Bienvenido Señor Usuario")
        raspiHabla("Por favor seleccione una de las siguientes opciones")
        raspiHabla("Diga 'Reportar estado de ánimo' para recomendarte algo según tu estado de ánimo")
        print(getKeyWords(reconocerVoz(7),list(Diccionario_sentimientos.keys())))



if __name__ == "__main__":
    main()