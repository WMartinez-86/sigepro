from django.test import Client
from django.contrib.auth.models import User
import unittest
from django.contrib.auth import SESSION_KEY

from django import setup
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'sigepro.settings'
setup()


# Create your tests here.
class SigeproTestSuite(unittest.TestCase):
    """
    Clase que implementa una suite para los test de Login de Usuario
    """

    def setUp(self):
        """
        Funcion que inicializa el test con Datos de Prueba sobre usuarios
        sobre datos de la BD
        """

        self.client = Client()
        self.username = 'manuel'
        self.email = 'smgalu@gmail.com'
        self.password = '12345'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)

    def tearDown(self):
        """
        @param self
        Llamado una vez finalizado el test
        """

        self.test_user.delete()

    def test_11(self):
        """
        Datos Correctos
        @param self
        @return self.assertEqual(login, True)
        """

        login = self.client.login(username=self.username, password=self.password)
        return self.assertEqual(login, True)

    def test_12(self):
        """
        Datos incorrectos sobre la Base de Datos
        @param self
        @return self.assertEquals(login, False)
        """

        login = self.client.login(username='Incorrecto', password='111')
        return self.assertEquals(login, False)

    def test_inicio(self):
        """Test para ver si puede entrar a la pagina de inicio
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def logout(self):
        """
        Test para el logout
        usuario = User.objects.create_user('juan', 'juan@pol.com', 'juanma')
        c = Client()
        c.login(username='juan', password='juanma')
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SESSION_KEY not in self.client.session)

        """
        User.objects.create_user('juan', 'juan@pol.com', 'juanma')
        c = Client()
        c.login(username='juan', password='juanma')
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SESSION_KEY not in self.client.session)