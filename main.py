from flask import request, make_response, redirect, render_template, session
import unittest
from flask_login import login_required
from app.firestore_service import get_users, get_todos

from app import create_app

app = create_app()


@app.cli.command() # cli = command line interface
def test():
    tests = unittest.TestLoader().discover('tests') # unittest va a buscar todos los test que tengamos en el directorio tests
    unittest.TextTestRunner().run(tests)


# Manejo de error 404.
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


# Manejo de error 500
@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)


# Ruta principal del FLASK.
@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


# Ruta que gestiona el archivo HTML hello.html
# El metodo GET, es un comando de flask para obtener respuestas del serv.
@app.route('/hello', methods=['GET'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username), # levanto los todos de firestore
        'username': username
    }

    users = get_users()

    for user in users:
        # Levanto los usuarios de firestore
        print(user.id)
        # Levanto las contraseñas de usuarios en firestore
        print(user.to_dict()['password'])

    return render_template('hello.html', **context)
    # al poner **variable, cuando el template recibe la variabl
    # la recibe ya "desplegada"
