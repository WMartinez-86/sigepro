from django.db import models
from django.contrib.auth.models import Group
from apps.flujos.models import Flujo
from django.contrib.auth.models import User
from apps.proyectos.models import Proyecto
from apps.sprints.models import Sprint


# Create your models here.


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
    @cvar proyecto: Clave foranea a un Proyecto
    @cvar desarrollador: Clave foranea a un Desarrollador
    @cvar fecha_mod: Clave foranea a a un Sprint
    @cvar actividad: Clave foranea a una Actividad
    """
    estado_choices = ((0, 'ToDo'), (1, 'Doing'), (2, 'Done'), (3, 'Pendiente Aprobacion'), (4, 'Aprobado'))
    nombre = models.CharField(max_length=20, verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripcion')
    prioridad = models.IntegerField(choices=((i, i) for i in range(1, 11)), default=1)
    valor_negocio = models.PositiveIntegerField(verbose_name='Valor de Negocio')
    valor_tecnico = models.PositiveIntegerField(verbose_name='Valor Tecnico')
    tiempo_estimado = models.PositiveIntegerField(verbose_name='Tiempo Estimado')
    tiempo_registrado = models.PositiveIntegerField(default=0, verbose_name='Tiempo Registrado')
    ultimo_cambio = models.DateTimeField(auto_now=True, verbose_name='Ultimo Cambio')
    estado = models.IntegerField(choices=estado_choices, default=0)
    proyecto = models.ForeignKey(Proyecto)
    desarrollador = models.ForeignKey(User, null=True, blank=True)
    #sprint = models.ForeignKey(Sprint, null=True, blank=True)
    #actividad = models.ForeignKey(Actividad, null=True, blank=True)


class Archivo(models.Model):
    """
    Modelo que representa a un Archivo
    @cvar archivo: Campo de tipo Archivo
    @cvar id_item: Clave foranea a Item
    @cvar nombre: Un campo de texto
    """
    archivo=models.FileField(upload_to='archivos')
    id_userStory=models.ForeignKey(UserStory, null=True)
    nombre=models.CharField(max_length=100, null=True)



