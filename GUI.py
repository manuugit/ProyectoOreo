from flask import Flask, render_template, request

app = Flask(__name__)

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

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        print(request.form.get('nombre'))
    return render_template('index.html', data = None)


@app.route('/gustos', methods=['GET','POST'])
def gustos():
    if request.method == 'GET':
        pass
    return render_template('gustos.html', data = Diccionario_gustos)

@app.route('/recomendacion', methods=['GET','POST'])
def recomendacion():
    if request.method == 'GET':
        pass
    return render_template('recomendacion.html', data = None)

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        pass
    return render_template('signup.html', data = None)

if __name__ == '__main__':
    app.run(debug=True)