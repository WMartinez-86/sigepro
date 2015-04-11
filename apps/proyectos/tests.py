from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.proyectos.models import Proyecto

# Create your tests here.
class sigeproTestCase(TestCase):
    fixtures = ["proyectos_testmaker"]



    def test_listar_proyectos(self):
        '''
         Test para ver si lista correctamente un proyecto
        '''
        print "\n\n--------Listando los proyectos-------"
        c = Client()
        c.login(username='juanma', password='juanma')
        #proyecto= Proyecto.objects.create(id=3, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
        resp = c.get('/proyectos/')
        self.assertEqual(resp.status_code, 200)
        print "Status 200, indica exito\n"
        self.assertEqual([proyecto.pk for proyecto in resp.context['datos']], [1, 2, 3, 4, 5, 6, 7])


    def test_detalle_proyectos(self):
        '''
        Test para visualizar los detalles de un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        print "\n--------Listando los detalles de un proyecto-------"
        #Test para proyecto existente
        resp = c.get('/proyectos/1')
        self.assertEqual(resp.status_code, 200)
        print "Status 200, indica exito\n"
        self.assertEqual(resp.context['proyecto'].pk, 1)
        self.assertEqual(resp.context['proyecto'].nombre, 'SIAP')

        #Test para proyecto inexistente
        print "\nMostrando un proyecto inexistente\n"
        resp = c.get('/proyectos/1000')
        self.assertEqual(resp.status_code, 404)


    def test_modficar_proyecto(self):
        '''
         Test para ver si modifica correctamente un proyecto
        '''
        c = Client()
        print "\n\n--------Se intenta modificar los proyectos-------"
        c.login(username='admin', password='admin')
        #test para verificar que si no modifica nada, no guarda
        resp = c.post('/proyectos/modificar/1')
        self.assertEqual(resp.status_code, 200)
        print "Status 200, indica exito, se redirige adecuadamente\n"


    def test_registrar(self):
        '''
         Test para ver si crea correctamente un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        print "-------------------Creando Proyectos-----"
        #prueba importar un proyecto y asignarle como nombre un nombre ya existente. Retorna un mensaje de nivel 20,
        #informando que ya existe un proyecto con ese nombre
        resp = c.post('/proyectos/registrar/', {'nombre': 'sigepro'})
        print "Crea correctamente el proyecto,  llena el formulario de la url /proyectos/registrar/ mediante el cual llama al metodo 'crear_rol' que recibe el request"
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['messages'].level, 20)

        #registra correctamente y redirige a la pagina indicada
        resp = c.post('/proyectos/registrar/',
                      {'nombre': 'Proyecto nuevo', 'descripcion': 'ds', 'observaciones': 'sdasd',
                       'fecha_ini': '20/02/2014', 'fecha_fin': '20/02/2015', 'lider': 1, 'comite': 1}, follow=True)
        self.assertEqual(resp.status_code, 200)
        #self.assertRedirects(resp, 'http://testserver/proyectos/register/success/')
        print "Status 200, indica exito en la operacion\n"
        #no registra correctamente ya que la fecha de inicio es despues de la de fin
        resp = c.post('/proyectos/registrar/',
                      {'nombre': 'Proyecto nuevo 2', 'descripcion': 'ds', 'observaciones': 'sdasd',
                       'fecha_ini': '20/02/2015', 'fecha_fin': '20/02/2014', 'lider': 1, 'comite': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['messages'].level, 20)


class ProyectoTest(TestCase):


    def setUp(self):
        print "\n-----------------TEST PROYECTO------------------------------"

        u4 = User.objects.create(username='pruebatest', first_name='runJoey', last_name='passit',
                                       password='pruebatest')

        Proyecto.objects.create(nombre='prueba', descripcion="Este es un proyecto",
                                           fecha_ini="2015-01-12",
                                           fecha_fin="2015-01-14",
                                           lider= u4,
                                           observaciones="esta es una observacion")
                                           #comite=crear_comite([u2, u3])
        print("Creo el proyecto mediante el metodo setUp()")