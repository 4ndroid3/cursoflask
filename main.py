from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest
from flask_login import login_required, current_user

from app import create_app
from app.forms import TodoForm, DeleteTodoForm
from app.firestore_service import get_users, get_todos, put_todo, delete_todo



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
@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    username = current_user.id
    todo_form = TodoForm()
    delete_form = DeleteTodoForm()

    context = {
        'user_ip': user_ip,
        'todos': get_todos(user_id=username), # levanto los todos de firestore
        'username': username,
        'todo_form': todo_form,
        'delete_form': delete_form
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username, descripcion=todo_form.descripcion.data)

        flash('Tu tarea se creo OK')

        return redirect(url_for('hello'))

    return render_template('hello.html', **context)
    # al poner **variable, cuando el template recibe la variabl
    # la recibe ya "desplegada"


@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)

    return redirect(url_for('hello'))
