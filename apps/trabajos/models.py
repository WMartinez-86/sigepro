from django.db import models
from apps.userStories.models import UserStory
from apps.sprints.models import Sprint
from django.utils.encoding import force_bytes
from base64 import b64encode
# Create your models here.

class Trabajo(models.Model):
    """
    modelo que representa un trabajo realizado en un US,
    guarda relacion con el sprint y el US
    @cvar userstory: relacion del trabajo con el UserStory
    @cvar sprint: relacion del trabajo con el sprint
    @cvar tipo_trabajo: indica el tipo de trabajo si es normal o un cambio de estado del US
    @cvar hora: tiempo de trabajo realizado
    @cvar descripcion: descripcion breve del trabajo realizado
    """

    TIPO_CHOICES = (
    (0, ('Normal')),
    (1, ('Cambio de estado')),
    )

    descripcion = models.TextField(max_length=140)
    userStory = models.ForeignKey(UserStory)
    tipo_trabajo = models.SmallIntegerField(choices=TIPO_CHOICES, default=0)
    hora = models.PositiveIntegerField(default=0)
    fecha = models.DateField(verbose_name='Fecha')

    def __str__(self):
        return self.descripcion


class Adjunto(models.Model):
    """
    Modelo que repsenta a un archivo
    @cvar binario: Campo de tipo binario que almacena el archivo adjunto
    @cvar id_trabajo: clave foranea a un trabajo en el cual se cargo el archivo
    @cvar nombre: un campo de texto con el nombre que representa el archivo
    """

    nombre = models.CharField(max_length=100, null=True)
    descripcion = models.TextField()
    binario = models.BinaryField(null=True, blank=True)
    fechaCreacion = models.DateTimeField(auto_now_add=True)
    trabajo = models.ForeignKey(Trabajo)



    def img64(self):
        return b64encode(force_bytes(self.binario))