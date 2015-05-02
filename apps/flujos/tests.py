from django.test import TestCase

from django.test import TestCase, Client
from apps.flujos.models import Flujo
from apps.proyectos.models import Proyecto
from django.contrib.auth.models import User




class FlujoTest(TestCase):


    def setUp(self):
        print "\nTEST FLUJO"

        u4 = User.objects.create(username='avelinaaa', first_name='runJoey', last_name='passit',
                                       password='fija')

        proyecto = Proyecto.objects.create(nombre='prueba', descripcion="Este es un proyecto",
                                           fecha_ini="2015-01-12",
                                           fecha_fin="2015-01-14",
                                           lider= u4,
                                           observaciones="esta es una observacion")

        flujoprueba = Flujo.objects.create(nombre='faseprueba', descripcion="Este es un flujo",
                            maxItems = 3,  fInicio="2015-01-12", orden = 3,
                            fCreacion="2015-01-10", proyecto = proyecto)
        flujoprueba.save()
        print("Creo el flujo mediante el metodo setUp")



    def test_ABMFlujo(self):
        valido=False
        print "\n----------Se procede a buscar la fase de prueba creada"
        valido = Flujo.objects.filter(nombre="flujoprueba").exists()
        if valido:
            print "\nSe encontro el flujo creada"
        if valido==False:
            print "\nNo se ha creado el flujo"
        print "\n----------Ahora se busca un flujo que no existe"
        valido=False
        valido=Proyecto.objects.filter(nombre="flujopruebanoexiste").exists()
        if valido==False:
            print "\nNo existe el flujo "
        print "\n----------Se procede a buscar el flujo creado para modificar su nombre"
        valido = Flujo.objects.filter(nombre="faseprueba").exists()
        if valido:
            print "\nSe encontro el flujo y se procedera a cambiar el valor del campo nombre"
            Flujo.objects.filter(nombre="flujoprueba").update(nombre ="nuevonombre")
            #faseMod.nombre = "nuevonombre"
            #faseMod.save()
            valido = Flujo.objects.filter(nombre="nuevonombre").exists()
            if valido:
                print "\nEl flujo fue modificada adecuadamente con nombre= nuevoNombre"

        print "\n----------Se procede a borrar el flujo "
        valido = False
        valido= Flujo.objects.filter(nombre="nuevoNNombre").exists()
        if valido:
                flu = Flujo.objects.filter(nombre="nuevoNNombre")
                flu.delete()
                print "\nFlujo Borrada"
        if valido==False:
             print "Error al borrar el flujo, se debe dar un nombre de flujo existente"