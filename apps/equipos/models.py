from django.db import models
from django.contrib.auth.models import User, Group
from apps.proyectos.models import Proyecto

# Create your models here.



class MiembroEquipo(models.Model):
    """
    Miembros del equipo de un proyecto con un rol específico
    @cvar usuario: Clave foranea a un Usuario
    @cvar proyecto: Clave foranea a un Proyecto
    @cvar roles: Clave muchos a muchos a Roles
    """

    usuario = models.ForeignKey(User)
    proyecto = models.ForeignKey(Proyecto)
    roles = models.ManyToManyField(Group)
    fuerza_trabajo = models.IntegerField(default=0)