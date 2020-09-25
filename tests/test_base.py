from flask_testing import TestCase
from flask import current_app, url_for

from main import app


class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # para hacer testing se lo debe desactivar
        
        return app
    
    # Primera prueba, prueba que la app de flask existe
    def test_app_exist(self):
        self.assertIsNotNone(current_app)
    
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING']) # Comprueba que la configuracion de la app este en modo testing

    def test_index_redirects(self):
        # Comprueba que index.html nos redirige a hello.html
        response = self.client.get(url_for('index'))

        self.assertRedirects(response, url_for('hello'))

    def test_hello_get(self):
        # el cod 200 es un msj de OK con el servidor.
        response = self.client.get(url_for('hello'))

        self.assert200(response)

    def test_hello_post(self):
        response = self.client.post(url_for('hello'))

        self.assertTrue(response.status_code, 405)

    def test_auth_blueprint_exists(self):
        self.assertIn('auth', self.app.blueprints)

    def test_auth_login_get(self):
        response = self.client.get(url_for('auth.login'))

        self.assert200(response)

    def test_auth_login_tempalte(self):
        self.client.get(url_for('auth.login'))

        self.assertTemplateUsed('login.html')

    def test_auth_login_post(self):
        # verificacion de un post
        # creo un usuario generico y se lo paso por parametros para
        # chequear que el cod se ejecuta OK.
        fake_form = {
            'username': 'fake',
            'password': 'fake-pasword'
        }

        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertRedirects(response, url_for('index'))