__author__ = 'smgalu'

from django.db import models
# from django.contrib.auth.models import User
# from apps.proyectos.models import Proyecto

# Create your models here.
class Rol(models.Model):
    """
    Clase del Modelo que a los roles con sus atributos.
    @cvar nombre : Cadena de caracteres
    """
    nombre = models.CharField(max_length=50)


    def __unicode__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.id:
            super(Rol, self).save(*args, **kwargs)