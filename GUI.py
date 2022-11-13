from flask import Flask, render_template, request, redirect, session, flash
from flask_session import Session
import sqlite3 #La BD
import pickle # Para abrir el modelo predictivo
import pandas as pd # manipulacion dataframes

# Este archivo, desde el punto de vista del MVC es el controlador, y gestiona la información entre la vista
# y el modelo, donde se trabaja la persistencia de datos.

# Para iniciarlizar una aplicación de flask se debe escribir esta instrucción
# __name__ es una variable del sistema que toma distintos valores en caso de que la ejecucion
# de el .py sea como un módulo (librería) o sea el programa principal en ejecucución.
app = Flask(__name__)

# Estos parametros hacen referencia a la sesión del usuario, para este caso las sesiones no son permanentes
# es decir, se cierran cuando el usuario cierra el navegador y son de archivos del sistema, alternativamente
# podrían ser en bases de datos.
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#BD
conn = sqlite3.connect("nombre_gustos.sqlite", check_same_thread=False)
cur = conn.cursor()

def insertarBD(sentencia):
    conn2 = sqlite3.connect("nombre_gustos.sqlite", check_same_thread=False)
    conn2.execute(sentencia)
    conn2.commit()
    conn2.close

#Modelo Predictivo y afines
archivoModelo = 'modeloPredictivoAvanzado.pkl'
modeloKNN, variablesModelo = pickle.load(open(archivoModelo, 'rb'))

def prediccionCluster(gustos, sentimientos):
    #Ajuste del dataframe para pasar por el modelo
    valores = pd.DataFrame()
    i = 0
    for gusto in gustos:
        valores.insert(i, gusto, [1])
        i = i+1
    for sentimiento in sentimientos:
        valores.insert(i, sentimiento, [1])
        i = i+1

    #Reindexamos con las variables del modelo / Se adicionan las columnas faltantes
    valores=valores.reindex(columns=variablesModelo,fill_value=0)


    #Realizamos la prediccion
    prediccion = modeloKNN.predict(valores)
    return prediccion[0]    
    
def Recomendar(cluster):
    #obtenemos el numero de cluster
    perfil = int(cluster[7:len(cluster)])
    #consulta de recomendacion según el cluster
    rec = cur.execute("select recomendacion from recomendaciones where idRecomendacion=?",(perfil,)).fetchone()[0]
    return rec

# Estos diccionarios son valores relacionados a el método de machine learning y son vitales para la funcionalidad
# del proyecto.
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


# Las aplicaciónes básicas de flask se manejan de una forma sencilla, definimos las rutas o endpoints de 
# nuestro aplicativo y los métodos posibles para cada endpoint, y para cada ruta creamos una función que hace el manejo
# de las vistas a renderizar.
@app.route('/', methods=['GET','POST'])
def index():
    mensaje = ""
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        # Cuando el usuario de la página esté en index.html (el login) y nos haga un post, vamos a almacenar su nombre en
        # la sesión correspondiente a él. Este nombre viene de un campo del formulario que tiene el campo de nombre 
        # (buscar el input) con name = "nombre".
        nombre = request.form.get("nombre")
        # validamos si el usuario está registrado en la bd
        valNombre = cur.execute("select nombre from usuarios where nombre=?",(nombre,)).fetchone()
        if valNombre == None:
            mensaje = "Este usuario no está registrado, por favor registrese"
        else:
            session["nombre"] = nombre
            return redirect("/gustos")
    # cuando se renderiza una plantilla en flask, el primer parámetro debe ser el nombre de la plantilla, y los parametros siguientes (opcionales)
    # son datos relevantes para la plantilla, estos datos pueden ser manejados desde el HTML usando código Python con una sintaxis especial.
    return render_template('index.html', data = mensaje)


@app.route('/gustos', methods=['GET','POST'])
def gustos():
    nombre = ""
    estado = ""
    if request.method == 'GET':
        # Si no tenemos un nombre en la sesión significaría que el usuario no se logueó, por lo tanto lo redirigimos al login.
        if not session.get("nombre"):
            return redirect("/")
        else:
        # Por propositos de aprendizaje, si el usuario está logueado imprimimos en la consola de Python su nombre
            print(session.get("nombre"))
            
    # obtenemos el id del usuario de la tabla usuarios
    nombre = session.get("nombre")        
    idUsuario = cur.execute("select * from usuarios where nombre=?",(nombre,)).fetchone()[0]

    # obtenemos los gustos del usuario desde la bd
    gustosActuales = cur.execute("SELECT gusto FROM gustos INNER JOIN usuarios ON gustos.idUsuario = usuarios.idUsuario WHERE nombre = ?",(nombre,)).fetchall()
    gustosActuales = list(map(lambda x: x[0],gustosActuales))
    # si el usuario ya tenía gustos registrados, deshabilitamos los check buttons y el botón
    # de esta forma el usuario puede consultarlos, pero no modificarlos
    if gustosActuales != []:
        estado = "disabled"
    if request.method == 'POST':
        # Cuando el usuario envíe el formulario obtenemos una lista con todos los gustos que seleccionó y los almacenamos
        # en la sesión. Luego lo redirigimos a la recomendación
        gustos=request.form.getlist('gusto')
        session["gustos"] = gustos
        print(session.get("gustos"))
        # insertamos los gustos seleccionados por el usuario en la bd
        for gusto in gustos:
            insertarBD("insert into gustos(gusto,idUsuario) values('{0}',{1})".format(gusto, idUsuario))
        return redirect("/recomendacion")
    # Para este endpoint es importante que sea cual sea la solicitud se mande el diccionario de gustos al HTML, para renderizar
    # cada gusto en un check button de una manera rápida y escalable.
    return render_template('gustos.html', data = Diccionario_gustos, gustosActuales = gustosActuales, estado = estado)

@app.route('/recomendacion', methods=['GET','POST'])
def recomendacion():
    if request.method == 'GET':
        pass

    if request.method == 'POST':
        # Cuando el usuario envíe el formulario de sentimientos hacemos similar a en gustos, obtener sus sentimientos y guardarlos en la 
        # sesion. Adicionalmente gracias a las facilidades de Python buscamos facilmente la moda en los sentimientos que seleccionó.
        
        nombre = session.get("nombre")
        
        # obtenemos los gustos del usuario
        gustosActuales = cur.execute("SELECT gusto FROM gustos INNER JOIN usuarios ON gustos.idUsuario = usuarios.idUsuario WHERE nombre = ?",(nombre,)).fetchall()
        gustosActuales = list(map(lambda x: x[0],gustosActuales))
        
        # obtenemos los sentimientos del usuario
        sentimientos=request.form.getlist('sentimiento')
        session["sentimientos"] = sentimientos
        sentimiento = None

        # obtenemos los valores de cada sentimiento de acuerdo con el diccionario, para poder calcular
        # el sentimiento universal más repetido en el usuario
        sentimientosM = []
        for sen in sentimientos:
            sentimientosM.append(Diccionario_sentimientos.get(sen))
        
        if sentimientosM:
            sentimiento = max(set(sentimientosM), key=sentimientosM.count)
        # -- TODO: ¡Añadir la linea de recomendación! --
        # Preparamos los datos para que coincidan con el formato del modelo y así poder unirlos
        # en un dataframe
        for i in range(0, len(gustosActuales)):
            gustosActuales[i] = gustosActuales[i].replace(' ', '_')
        for i in range(0, len(sentimientos)):
            sentimientos[i] = "Diario."+sentimientos[i]

        print(sentimientos)
        # integramos el modelo predictivo para hacer la recomendación
        clusterAsignado = prediccionCluster(gustosActuales, sentimientos)
        recomendacion = Recomendar(clusterAsignado) 
        # Para este caso es importante mandar dos parámetros a la hora de renderizar la plantilla, el primero es el diccionario de 
        # sentimientos para renderizar cada sentimiento de forma facil y escalable, y el segundo es la moda para renderizar una sección 
        # adicional de código en el html.
        return render_template('recomendacion.html', data = Diccionario_sentimientos, sentimiento=sentimiento, recomendacion = recomendacion)
    return render_template('recomendacion.html', data = Diccionario_sentimientos, sentimiento = None, recomendacion = None)

@app.route('/signup', methods=['GET','POST'])
def signup():
    mensaje = ""
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        nombre = request.form.get("nombre")
        valNombre = cur.execute("select nombre from usuarios where nombre=?",(nombre,)).fetchone()
        # si el usuario no estaba registrado, lo insertamos en la bd
        if valNombre==None:
            insertarBD("insert into usuarios(nombre) values('{0}')".format(nombre))
            session["nombre"] = nombre
            return redirect("/gustos")
        else:
            mensaje = "Este usuario ya está registrado" 
    return render_template('signup.html', data = mensaje)


@app.route('/logout', methods=['GET','POST'])
# Este endpoint es un endpoint especial en el que no vamos a renderizar contenido, si no que vamos a realizar operaciónes de backend.
def logout():
    # Cuando el usuario llegue a este endpoint su sesión se cerrará, simplemente quitando su nombre.
    session["nombre"] = None
    return redirect("/")

# Cuando el .py sea ejecutado como programa, correr la app.
if __name__ == '__main__':
    app.run(debug=True)