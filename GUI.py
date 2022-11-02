from flask import Flask, render_template, request

app = Flask(__name__)

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
    return render_template('gustos.html', data = None)

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