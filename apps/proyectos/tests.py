from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from apps.proyectos.models import Proyecto
from django.contrib.auth.models import Permission
from django.utils import timezone

import django
django.setup()


__author__ = 'juanma'
# Create your tests here.
class sigeproTestCase(TestCase):
    fixtures = ["proyectos_testmaker"]


class ProjectTest(TestCase):

    def setUp(self):
        u = User.objects.create_superuser('superUsuario','superUsuario@email.com', 'superUsuario')
        #p = Permission.objects.get(codename='add proyecto')
        #u.user_permissions.add(p)
        #p = Permission.objects.get(codename='change proyecto')
        #u.user_permissions.add(p)
        #p = Permission.objects.get(codename='delete proyecto')
        #u.user_permissions.add(p)
        u = User.objects.create_user('fulano','superUsuario@email.com', 'superUsuario')
        pro= Proyecto.objects.create(nombreCorto='Proyecto', nombre='Proyecto Largo', estado='ELI',fecha_ini=timezone.now(),fecha_fin=timezone.now(),fecha_creacion='2015-04-30 12:00',duracion_sprint='30', descripcion='Descripcion el prctooye')
        Group.objects.create(name='rol')

    # def test_permission_to_create_proyecto(self):
    #     c = self.client
    #     self.assertTrue(c.login(username='superUsuario', password='superUsuario'))
    #     response = c.get('/proyectos/registrar')
    #     self.assertEquals(response.status_code, 200)

    # def test_permission_to_change_proyecto(self):
    #     Sc = self.client
    #     self.assertTrue(c.login(username='superUsuario', password='superUsuario'))
    #     response = c.get('/projects/1/edit/')
    #     self.assertEquals(response.status_code, 200)
    #
    # def test_permission_to_delete_proyecto(self):
    #     c = self.client
    #     self.assertTrue(c.login(username='superUsuario', password='superUsuario'))
    #     response = c.get('/projects/1/delete/')
    #     self.assertEquals(response.status_code, 200)
    #
    # def test_not_permission_to_create_proyecto(self):
    #     c = self.client
    #     self.assertTrue(c.login(username='fulano', password='superUsuario'))
    #     response = c.get('/projects/add/')
    #     self.assertEquals(response.status_code, 403)
    #
    # def test_not_permission_to_change_proyecto(self):
    #     c = self.client
    #     self.assertTrue(c.login(username='fulano', password='superUsuario'))
    #     response = c.get('/projects/1/edit/')
    #     self.assertEquals(response.status_code, 403)
    #
    # def test_not_permission_to_delete_proyecto(self):
    #     c = self.client
    #     self.assertTrue(c.login(username='fulano', password='superUsuario'))
    #     response = c.get('/projects/1/delete/')
    #     self.assertEquals(response.status_code, 403)


    # def test_create_proyecto(self):
    #     c = self.client
    #     self.assertTrue(c.login(username='sergio', password='sigepro'))
    #     response = c.get('/proyectos/registrar/')
    #     self.assertEquals(response.status_code, 200)
    #     response = c.post('/proyectos/registrar', {'nombreCorto': 'test', 'nombre': 'test_proyecto',
    #                                         'descripcion': 'test', 'duracion_sprint': 30, 'fecha_ini': timezone.now(),
    #                                         'fecha_fin': timezone.now()})
    #     #self.assertRedirects(response, '/PROYECTOS/{}/'.format(p.id))

    def test_edit_proyecto(self):
        c = self.client
        self.assertTrue(c.login(username='sergio', password='sigepro'))
        response = c.get('/proyectos/modificar/1')
        self.assertEquals(response.status_code, 200)
        #response = c.post('/projects/1/edit/', {'nombreCorto': 'Poyecto', 'nombre': 'Royecto Largo', 'estado': 'Inactivo', 'fecha_ini': timezone.now(), 'fecha_fin': timezone.now(), 'fecha_creacion': '2015-03-10 18:00', 'duracion_sprint': '30', 'descripcion': 'Prueba numero 800'}, follow=True)
        p = Proyecto.objects.get(pk=1)
        p.nombreCorto = 'Proyec'
        p.save(update_fields=['nombreCorto'])
        #deberia redirigir
        self.assertEquals(response.status_code, 200)
        self.assertIsNotNone(Proyecto.objects.get(nombreCorto='Proyec'))

    def test_delete_proyecto(self):
        c = self.client
        self.assertTrue(c.login(username='superUsuario', password='superUsuario'))
        response = c.get('/projects/1/delete/')
        self.assertEquals(response.status_code, 200)
        response = c.post('/projects/1/delete/', {'Confirmar':True}, follow=True)
        p = Proyecto.objects.get(pk=1)
        p.delete()
        self.assertRedirects(response, '/projects/')
        #ahora ya no deberia existir el registro
        response = c.get('/projects/1/')
        self.assertEquals(response.status_code, 404)


    # def test_listar_proyectos(self):
    #     '''
    #      Test para ver si lista correctamente un proyecto
    #     '''
    #     print "\n\n--------Listando los proyectos-------"
    #     c = Client()
    #     c.login(username='admin', password='admin')
    #     #proyecto= Proyecto.objects.create(id=3, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
    #     resp = c.get('/proyectos/')
    #     self.assertEqual(resp.status_code, 200)
    #     print "Status 200, indica exito\n"
    #     self.assertEqual([proyecto.pk for proyecto in resp.context['datos']], [1, 2, 3, 4, 5, 6, 7])


    # def test_detalle_proyectos(self):
    #     '''
    #     Test para visualizar los detalles de un proyecto
    #     '''
    #
    #     c = Client()
    #     c.login(username='admin', password='admin')
    #     print "\n--------Listando los detalles de un proyecto-------"
    #     #Test para proyecto existente
    #     resp = c.get('/proyectos/2')
    #     self.assertEqual(resp.status_code, 200)
    #     print "Status 200, indica exito\n"
    #     self.assertEqual(resp.context['proyecto'].pk, 2)
    #     self.assertEqual(resp.context['proyecto'].nombre, 'sigepro')
    #
    #     #Test para proyecto inexistente
    #     print "\nMostrando un proyecto inexistente\n"
    #     resp = c.get('/proyectos/1000')
    #     self.assertEqual(resp.status_code, 404)


    # def test_modficar_proyecto(self):
    #     '''
    #      Test para ver si modifica correctamente un proyecto
    #     '''
    #     c = Client()
    #     print "\n\n--------Se intenta modificar los proyectos-------"
    #     c.login(username='admin', password='admin')
    #     #test para verificar que si no modifica nada, no guarda
    #     resp = c.post('/proyectos/modificar/1')
    #     self.assertEqual(resp.status_code, 200)
    #     print "Status 200, indica exito, se redirige adecuadamente\n"


    # def test_registrar(self):
    #     '''
    #      Test para ver si crea correctamente un proyecto
    #     '''
    #
    #     c = Client()
    #     c.login(username='admin', password='admin')
    #     print "-------------------Creando Proyectos-----"
    #     #prueba importar un proyecto y asignarle como nombre un nombre ya existente. Retorna un mensaje de nivel 20,
    #     #informando que ya existe un proyecto con ese nombre
    #     resp = c.post('/proyectos/registrar/', {'nombre': 'mesa'})
    #     print "Crea correctamente el proyecto,  llena el formulario de la url /proyectos/registrar/ mediante el cual llama al metodo 'crear_rol' que recibe el request"
    #     self.assertEqual(resp.status_code, 200)
    #
    #     self.assertEqual(resp.context['messages'].level, 20)
    #
    #     #registra correctamente y redirige a la pagina indicada
    #     resp = c.post('/proyectos/registrar/',
    #                   {'nombre': 'Proyecto nuevo', 'descripcion': 'ds', 'observaciones': 'sdasd',
    #                    'fecha_ini': '20/02/2014', 'fecha_fin': '20/02/2015', 'lider': 1, 'comite': 1}, follow=True)
    #     self.assertEqual(resp.status_code, 200)
    #     #self.assertRedirects(resp, 'http://testserver/proyectos/register/success/')
    #     print "Status 200, indica exito en la operacion\n"
    #     #no registra correctamente ya que la fecha de fecha_ini es despues de la de fecha_fin
    #     resp = c.post('/proyectos/registrar/',
    #                   {'nombre': 'Proyecto nuevo 2', 'descripcion': 'ds', 'observaciones': 'sdasd',
    #                    'fecha_ini': '20/02/2015', 'fecha_fin': '20/02/2014', 'lider': 1, 'comite': 1})
    #     self.assertEqual(resp.status_code, 200)
    #     self.assertEqual(resp.context['messages'].level, 20)
