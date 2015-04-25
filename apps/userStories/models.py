from django.db import models
from django.contrib.auth.models import Group
from apps.flujos.models import Flujo

# Create your models here.
ESTADOS = (
    ('PEN','Pendiente'),#abierta
    ('CON','En Construccion'),#desarrollo
    ('FIN','Finalizado'),#cerrado cuando en una linea base
    ('VAL','Validado'),#iniciado o aprobado
    ('REV','Revision'),#revisar
    ('ANU','Anulado'),#inactivo
    ('BLO','Bloqueado')
)

class UserStories(models.Model):
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
    tiempo=models.PositiveIntegerField(verbose_name='Tiempo')
    estado=models.CharField(max_length=3,choices=ESTADOS, verbose_name='Estado')
    prioridad=models.IntegerField(verbose_name='Prioridad')
    #nota=models.TextField(max_length=140, verbose_name='Nota')
    fecha_creacion=models.DateField(verbose_name='Fecha de Creacion')
    fecha_mod=models.DateField(verbose_name='Fecha de Modificacion')
    flujo=models.ForeignKey(Flujo)
