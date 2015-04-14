from django.db import models
#from django.contrib.auth.models import usuarios

# Create your models here.

__author__ = 'juanma'

ESTADOS = (

    ('PEN', 'Pendiente'),
    ('ANU','Anulado'),
    ('ACT', 'Activo'),
    ('FIN','Finalizado'),
    ('ELI','Eliminado'),
)

class Proyecto(models.Model):
    """
    Clase del Modelo que representa al proyecto con sus atributos.
    @cvar nombre: Cadena de caracteres
    @cvar siglas: siglas del nombre del proyecto
    @cvar descripcion: Un campo de texto
    @cvar  fecha_ini: Fecha que indica el inicio de un proyecto
    @cvar fecha_fin: Fecha que indica el fin estimado de un proyecto
    @cvar estado: Enum de los tipos de estados por los que puede pasar un proyecto: Pendiente, Anulado, Activo y Finalizado
    @cvar cliente: Clave foranea a la tabla usuario
    """

    nombre= models.CharField(max_length=100, verbose_name='Nombre',unique=True)
    siglas= models.CharField(max_length=20)
    descripcion= models.TextField(verbose_name='Descripcion')
    fecha_ini=models.DateField(verbose_name='Fecha de inicio',null=False)
    fecha_fin=models.DateField(verbose_name='Fecha de Finalizacion',null=False)
    estado=models.CharField(max_length=3,choices= ESTADOS, default='PEN')

