from django.db import models
from django.contrib.auth.models import User, Group
from apps.proyectos.models import Proyecto

# Create your models here.



class MiembroEquipo(models.Model):
    """
    Miembros del equipo de un proyecto con un rol especifico
    @cvar usuario: Clave foranea a un Usuario
    @cvar proyecto: Clave foranea a un Proyecto
    @cvar roles: Clave muchos a muchos a Roles
    """

    usuario = models.ForeignKey(User)
    proyecto = models.ForeignKey(Proyecto, null = True)
    rol = models.ManyToManyField(Group)
    horasPorDia = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.proyecto.nombre
