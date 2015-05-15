from django.db import models
from apps.flujos.models import Flujo

# Create your models here.

class Actividad(models.Model):
    """
    Las actividades representan las distintas etapas de las que se componen un flujo
    """
    nombre = models.CharField(max_length=20)
    flujo = models.ForeignKey(Flujo)
    orden = models.IntegerField(default=0)



    def __str__(self):
        return self.nombre