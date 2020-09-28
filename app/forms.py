from flask_wtf import FlaskForm # importo wtf
from wtforms.fields import StringField, PasswordField, SubmitField # Importo los modulos para usar en forms
from wtforms.validators import DataRequired


# Extiendo FlaskForm, para usar todas las funciones de WTF
class LoginForm(FlaskForm): 
    username = StringField('Nombre de usuario', validators=[DataRequired()]) # los validators se usan para alertar si el usuario no completo el campo
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar') # Creo un botón


class TodoForm(FlaskForm):
    descripcion = StringField('Descripcion', validators=[DataRequired()])
    submit = SubmitField('Crear')


class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')


class UpdateTodoForm(FlaskForm):
    submit = SubmitField('Actualizar')