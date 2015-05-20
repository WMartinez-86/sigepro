from django.db import models
from django.contrib.auth.models import Group
from apps.flujos.models import Flujo
from django.contrib.auth.models import User
from apps.proyectos.models import Proyecto
from apps.sprints.models import Sprint
from apps.actividades.models import Actividad
#from apps.trabajos.models import Trabajo


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
    estados_kanban = ((0, 'ToDo'), (1, 'Doing'), (2, 'Done'), (3, 'Pendiente Aprobacion'), (4, 'Aprobado'))
    estados_scrum = ((0, 'Nuevo'), (1, 'Iniciado'), (2, 'Suspendido'), (3, 'Eliminado'))
    nombre = models.CharField(max_length=20, verbose_name='Nombre')
    descripcion = models.TextField(verbose_name='Descripcion')
    prioridad = models.IntegerField(choices=((i, i) for i in range(1, 10)), default=1)
    valor_negocio = models.PositiveIntegerField(verbose_name='Valor de Negocio')
    valor_tecnico = models.PositiveIntegerField(verbose_name='Valor Tecnico')
    tiempo_estimado = models.PositiveIntegerField(verbose_name='Tiempo Estimado')
    ultimo_cambio = models.DateTimeField(auto_now=True, verbose_name='Ultimo Cambio')
    estadoKanban = models.IntegerField(choices=estados_kanban, default=0)
    estadoScrum = models.IntegerField(choices=estados_scrum, default=0)
    proyecto = models.ForeignKey(Proyecto)
    flujo = models.ForeignKey(Flujo, null=True, blank=True)
    actividad = models.ForeignKey(Actividad, null=True, blank=True)
    #trabajo = models.ForeignKey(Trabajo, null=True, blank=True)


    def __str__(self):
        return self.nombre



