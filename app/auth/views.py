from flask import render_template, session, redirect, flash, url_for

from app.forms import LoginForm

from . import auth

# El metodo POST, es un comando de flask para obtener devoluciones del serv.
@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form' : LoginForm()
    }

    if login_form.validate_on_submit():
        username = login_form.username.data
        session['username'] = username
        flash('Nombre de usuario registrado con éxito')

        return redirect(url_for('index'))

    return render_template('login.html', **context)