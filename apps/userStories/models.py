from django.db import models
from django.contrib.auth.models import Group
from apps.flujos.models import Flujo
from django.contrib.auth.models import User



# Create your models here.
ESTADOS = (
    ('TODO','To Do'),#Por hacer
    ('DOING','Doing'),#desarrollo
    ('DONE','Done'),#Terminado
    ('FIN','Fin'),#Finalizado
)


class UserStory(models.Model):
    """
    Modelo que representa a un Item
    @cvar nombre: Cadena de caracteres
    @cvar descripcion: Un campo de texto
    @cvar costo: Entero positivo que representa el costo del item
    @cvar tiempo: Entero positivo que representa la cantidad de tiempo en dias
    @cvar estado: Enum de los tipos de estados por los que puede pasar una fase: Pendiente, En Construccion, Finalizado, Validado, Revision, Anulado
    @cvar version: Entero corto con valores positivos
    @cvar orden: Entero corto que representa el orden relative de items
    @cvar relacion: clave foranea a otro item
    @cvar tipo: Enum de los tipos de relaciones entre items: Padre-Padre-Antecesor-Padre
    @cvar fecha_creacion: Tipo de dato Date
    @cvar fecha_mod: Tipo de dato Date
    @cvar tipo_item: clave foranea a tipo item
    """
    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    descripcion=models.TextField(max_length=140, verbose_name='Descripcion')
    #costo=models.PositiveIntegerField(verbose_name='Costo')
    tiempoEstimado=models.PositiveIntegerField(verbose_name='Tiempo Estimado')
    tiempoReal=models.PositiveIntegerField(verbose_name='Tiempo Real')
    estado=models.CharField(max_length=3,choices=ESTADOS, verbose_name='Estado')
    #version=models.PositiveSmallIntegerField(verbose_name='Version')
    #relacion=models.ForeignKey('self',null=True, verbose_name='Relacion', related_name='relacionItem')
    #tipo=models.CharField(null=True,max_length=10, choices=TIPOS, verbose_name='Tipo')
    fecha_creacion=models.DateField(verbose_name='Fecha de Creacion')
    fecha_mod=models.DateField(verbose_name='Fecha de Modificacion')
    flujo=models.ForeignKey(Flujo)
    usuario=models.ForeignKey(User)
    #lineaBase=models.ForeignKey(LineaBase, null=True)

class Archivo(models.Model):
    """
    Modelo que representa a un Archivo
    @cvar archivo: Campo de tipo Archivo
    @cvar id_item: Clave foranea a Item
    @cvar nombre: Un campo de texto
    """
    archivo=models.FileField(upload_to='archivos')
    id_item=models.ForeignKey(UserStory, null=True)
    nombre=models.CharField(max_length=100, null=True)
