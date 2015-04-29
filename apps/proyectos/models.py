from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ValidationError
#from django.contrib.auth.models import usuarios

# Create your models here.

__author__ = 'juanma'

estados = (

    ('PRO', 'En Produccion'),
    ('CAN','Cancelado'),
    ('APR', 'Aprobado'),
    ('FIN','Finalizado'),
    ('ELI','Eliminado'),
)


class Proyecto(models.Model):
    """
    Modelo de Proyecto del sistema.

    Clase del Modelo que representa al proyecto con sus atributos.
    @cvar nombre: Cadena de caracteres
    @cvar siglas: siglas del nombre del proyecto
    @cvar descripcion: Un campo de texto
    @cvar  fecha_ini: Fecha que indica el inicio de un proyecto
    @cvar fecha_fin: Fecha que indica el fin estimado de un proyecto
    @cvar estado: Enum de los tipos de estados por los que puede pasar un proyecto: Pendiente, Anulado, Activo y Finalizado
    @cvar cliente: Clave foranea a la tabla usuario

    """
    nombre_corto = models.CharField(max_length=20)
    nombre_largo = models.CharField(max_length=40)
    estado = models.CharField(choices=estados, max_length=2, default='IN')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    fecha_creacion = models.DateField(auto_now_add=True)
    duracion_sprint = models.PositiveIntegerField(default=30)
    descripcion = models.TextField()
    #equipo = models.ManyToManyField(User, through='MiembrosEquipo')

    class Meta:
        #Los permisos estaran asociados a los proyectos, por lo que todos los permisos de ABM de las entidades
        #dependientes del proyecto, deben crearse como permisos de proyecto
        #en vez de 'add', 'change' y 'delete', los permisos personalizados seran 'create', 'edit' y 'remove' para
        #evitar confusiones con los por defecto.

        permissions = (
            ('list_all_projects', 'listar los proyectos disponibles'),
            ('view_project', 'ver el proyecto'),

            ('create_sprint', 'agregar sprint'),
            ('edit_sprint', 'editar sprint'),
            ('remove_sprint', 'eliminar sprint'),

            ('create_flujo', 'agregar flujo'),
            ('edit_flujo', 'editar flujo'),
            ('remove_flujo', 'eliminar flujo'),

            ('create_userstory', 'agregar userstory'),
            ('edit_userstory', 'editar userstory'),
            ('remove_userstory', 'eliminar userstory'),
            #TODO: Hace falta definir permisos para Versiones, Notas y Adjuntos?
        )

    def __unicode__(self):
        return self.nombre_corto

    def get_absolute_url(self):
        return reverse_lazy('project:project_detail', args=[self.pk])

    def clean(self):
        try:
            if self.inicio > self.fin:
                raise ValidationError({'inicio': 'Fecha de inicio no puede ser mayor '
                                                 'que la fecha de finalizacion.'})
        except TypeError:
            pass  # si una de las fechas es null, clean_field() se encarga de lanzar error