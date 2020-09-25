from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest
from app.firestore_service import get_users, get_todos

from app import create_app

app = create_app()

@app.cli.command() # cli = command line interface
def test():
    tests = unittest.TestLoader().discover('tests') # unittest va a buscar todos los test que tengamos en el directorio tests
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html',error=error)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET'])
def hello():
    user_ip = session.get('user_ip')
    username = session.get('username')

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username),
        'username': username
    }

    users = get_users()

    users = get_users()
    for user in users:
        print(user.id)
        print(user.to_dict()['password'])
      
    return render_template('hello.html', **context)
    # al poner **variable, cuando el template recibe la variabl
    # la recibe ya "desplegada"