from select import select
from tokenize import String
import speech_recognition as sr
import pyttsx3
import pandas as pd # manipulacion dataframes
import numpy as np  # matrices y vectores
#import matplotlib.pyplot as plt #gráfica
import sqlite3 #La BD
# from aiy.board import Board, Led

r = sr.Recognizer()
engine = pyttsx3.init()
Diccionario_sentimientos = {'Confundido':'Confusion',
    'Vacío':'Hipotimia',
    'Solo':'Hipotimia',
    'Estresado':'Estres',
    'Angustiado':'Hipotimia',
    'Eufórico':'Euforia',
    'Ansioso':'Ansiedad',
    'Tranquilo':'Tranquilidad',
    'Emocionado':'Energico',
    'Asustado':'Ansiedad',
    'Decepcionado':'Hipotimia',
    'Desesperado':'Ansiedad',
    'Enérgico':'Energico',
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
    'Decaído':'Decaido'}

Diccionario_gustos = {1:'Actividad Física',
    2:'Gastronomía',
    3:'Arte',
    4:'Películas y Series',
    5:'Videojuegos',
    6:'Lectura',
    7:'Idiomas',
    8:'Meditación',
    9:'Socializar',
    10:'Salir al aire libre',
    11:'Viajar',
    12:'Jugar con animales',
    13:'Dormir',
    14:'Música',
    15:'Estudiar',
    16:'Fotografía',
    17:'Baile',
    18:'Cantar',
    19:'Redes Sociales',
    20:'Coleccionismo',
    21:'Conducción',
    22:'Trabajar',
    23:'Ayuda Social',
    24:'Compras',
    25:'Maquillaje',
    26:'Juegos de mesa'}

conn = sqlite3.connect("nombre_gustos.sqlite")
cur = conn.cursor()

def insertarBD(sentencia):
    conn2 = sqlite3.connect("nombre_gustos.sqlite")
    conn2.execute(sentencia)
    conn2.commit()
    conn2.close

def creacionTablasBD():
    listOfTables = cur.execute(
        """SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%';""").fetchall()
    if(listOfTables==[]):
        cur.execute("""create table usuarios(
            idUsuario integer primary key AUTOINCREMENT,
            nombre text not NULL);""")
        cur.execute(""" create table gustos(
            idGusto integer primary key AUTOINCREMENT,
            gusto text not NULL,
            idUsuario integer,
            foreign key(idUsuario) references usuarios(idUsuario)
        );""")


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


def cambiarUltimaLetra(palabra, letra) -> String:
    palabraNueva = ""
    palabraNueva = palabra[:len(palabra)-1]+letra
    return palabraNueva

def prepararArray(array) : #estandariza las keywords para que queden en un solo género
    for i in range(len(array)):
        array[i] = cambiarUltimaLetra(array[i],'o')

def getKeyWords(text,array): #Texto de usuario, Array de posibles respuestas
    retArray = []
    text = text.upper()
    print(text)
    for palabra in array:
        palabre = cambiarUltimaLetra(palabra,'a')
        # palabre[len(palabre)-1] = 'a'
        if text.__contains__(palabra.upper()):
            retArray.append(palabra)
        if text.__contains__(palabre.upper()):
            retArray.append(palabre)

    prepararArray(retArray)

    if retArray == []:
        return "No hay elementos"       
    return retArray

    
def main():
    inicializarEngine()
    creacionTablasBD()
    while True:
        raspiHabla("Bienvenido Señor Usuario")
        raspiHabla("Por favor cuando el botón se ilumine, presionelo y diga su nombre.")
        #Esperar click de botón
        nombre = reconocerVoz(3)
        #On realease de botón
        raspiHabla("Hola "+nombre+", esta tu nombre correcto?")
        #Validación por medio de interacción con botón para tener el nombre correcto de usuario

        #Obtener nombre si existe en la BD
        valNombre = cur.execute("select nombre from usuarios where nombre=?",(nombre,)).fetchone()
        #Si el nombre no existe se trata de un usuario nuevo
        if(valNombre==None):
            insertarBD("insert into usuarios(nombre) values('{0}')".format(nombre))
            idUsuario = cur.execute("select * from usuarios where nombre=?",(nombre,)).fetchone()[0]

            raspiHabla(nombre+" selecciona cuales son tus gustos ingresando los numeros\nPresione z para confirmar:")
            
            for x, y  in Diccionario_gustos.items():
                print(x,". ",y)

            while(True):
                opcion = input()
                if(opcion.upper()=='Z'):
                    break
                elif(int(opcion) >0 and int(opcion)<27):
                    insertarBD("insert into gustos(gusto,idUsuario) values('{0}',{1})".format(Diccionario_gustos.get(int(opcion)), idUsuario))
                                
        else:
            gustos = cur.execute("SELECT gusto FROM gustos INNER JOIN usuarios ON gustos.idUsuario = usuarios.idUsuario WHERE nombre = ?",(nombre,)).fetchall()
            gustos = list(map(lambda x: x[0],gustos))
            print(gustos)

        # raspiHabla("Diga 'Reportar estado de ánimo' para recomendarte algo según tu estado de ánimo")
        # print(getKeyWords(reconocerVoz(7),list(Diccionario_sentimientos.keys())))
        



if __name__ == "__main__":
    main()