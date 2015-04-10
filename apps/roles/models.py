__author__ = 'smgalu'

from django.db import models

# Create your models here.


class Rol(models.Model):
    """
    Clase del Modelo que a los roles con sus atributos.
    @int id : Identificador
    @cvar nombre : Cadena de caracteres
    @cvar crear_usuario: Campo booelano
    """
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    #Permisos
    crear_usuario= models.BooleanField(default=False,verbose_name='Crear Usuario')
    modificar_usuario= models.BooleanField(default=False,verbose_name='Crear Usuario')
    consultar_usuario= models.BooleanField(default=False,verbose_name='Consultar Usuario')

    crear_rol= models.BooleanField(default=False,verbose_name='Crear Rol')
    modificar_rol= models.BooleanField(default=False,verbose_name='Modificar Rol')
    eliminar_rol= models.BooleanField(default=False,verbose_name='Eliminar Rol')
    consultar_rol= models.BooleanField(default=False,verbose_name='Consultar Rol')

    crear_userStory= models.BooleanField(default=False,verbose_name='Crear User Story')
    modificar_userStory= models.BooleanField(default=False,verbose_name='Modificar User Story')
    consultar_userStory= models.BooleanField(default=False,verbose_name='Consultar User Story')
    cambiarEstado_userStory= models.BooleanField(default=False,verbose_name='Cambiar Estado User Story')

    #Permisos de Proyecto incluyen flujos y actividades
    crear_proyecto= models.BooleanField(default=False,verbose_name='Crear Proyecto')
    modificar_proyecto= models.BooleanField(default=False,verbose_name='Modificar Proyecto')
    consultar_proyecto= models.BooleanField(default=False,verbose_name='Consultar Proyecto')

    def __unicode__(self):
        return self.nombre

    # def save(self, *args, **kwargs):
        #if not self.id:
        # super(Rol, self).save(*args, **kwargs)