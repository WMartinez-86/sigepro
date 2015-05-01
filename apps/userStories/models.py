from django.db import models
from django.contrib.auth.models import Group
from apps.flujos.models import Flujo
from django.contrib.auth.models import User
from apps.proyectos.models import Proyecto


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
    estado_choices = ((0, 'ToDo'), (1, 'Doing'), (2, 'Done'), (3, 'Pendiente Aprobacion'), (4, 'Aprobado'))
    nombre = models.CharField(max_length=20, verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripcion')
    prioridad = models.IntegerField(choices=((i, i) for i in range(1, 11)), default=1)
    valor_negocio = models.IntegerField(verbose_name='Valor de Negocio')
    valor_tecnico = models.IntegerField(verbose_name='Valor Tecnico')
    tiempo_estimado = models.PositiveIntegerField(verbose_name='Tiempo Estimado')
    tiempo_registrado = models.PositiveIntegerField(default=0, verbose_name='Tiempo Registrado')
    ultimo_cambio = models.DateTimeField(auto_now=True, verbose_name='Ultimo Cambio')
    estado = models.IntegerField(choices=estado_choices, default=0)
    proyecto = models.ForeignKey(Proyecto)
    desarrollador = models.ForeignKey(User, null=True, blank=True)
    #sprint = models.ForeignKey(Sprint, null=True, blank=True)
    #actividad = models.ForeignKey(Actividad, null=True, blank=True)



