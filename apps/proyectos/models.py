from django.db import models
#from django.contrib.auth.models import usuarios

# Create your models here.

__author__ = 'juanma'

ESTADOS = (

    ('NUE', 'Nuevo'), # cuando se crea
    ('PRO', 'Produccion'), # cuando se inicia
    ('FIN','Finalizado'), # cuando se termina
    ('APR', 'Aprobado'), # cuando se aprueba uno finalizado
    ('ELI','Eliminado'), # cuando se elimina o cancela
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

    nombre= models.CharField(max_length=50, verbose_name='Nombre',unique=True)
    nombreCorto= models.CharField(max_length=20, verbose_name='Nombre corto',unique=True)
    descripcion= models.TextField(verbose_name='Descripcion')
    fecha_ini=models.DateField(verbose_name='Fecha de inicio', null=True)
    fecha_fin=models.DateField(verbose_name='Fecha de Finalizacion', null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado=models.CharField(max_length=3,choices= ESTADOS, default='NUE')
    #duracion_sprint = models.PositiveIntegerField(default=30)
    #equipo = models.ManyToManyField(User, through='MiembroEquipo')

    def __str__(self):
        return self.nombre

    class Meta:
        default_permissions = ()
        verbose_name = 'proyecto'
        verbose_name_plural = 'proyectos'
