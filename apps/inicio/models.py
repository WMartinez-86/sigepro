from django.db import models
from django.contrib.auth.models import User



class Perfiles(models.Model):
    """
    Extiende del modelo User e incluye otros campos y funciones
    Los atributos de Usuario son
    @cvar usuario: Un atributo relacionado a la clase User de DjangoAdmin
    @cvar telefono: Un atributo entero
    @cvar direccion: Cadena de caracteres
    @cvar lider: valor binario que indica si tiene este perfil, por defecto es falso
    """
    
    usuario = models.OneToOneField(User)
    telefono = models.IntegerField(default=0,blank=True)
    '''
       telefono es numero telefonico perteneciente al usuario
    '''
    direccion = models.CharField(max_length=64,default='tu direccion',blank=True)
    '''
       direccion es direccion en la cual reside el usuario
    '''
    lider = models.BooleanField(null=False, default=0)
    '''
       representa si el usuario en cuestion es Scrum Master o no
    '''
    #foto = models.ImageField(upload_to='foto_usuario')
    # """
    #    Carga la foto del usuario y lo aloja en la carpeta foto_usuario
    #    necesidad de instalacion del PIL(Python Imaging LIbrary):
    #    http://www.mlewislogic.com/2011/09/how-to-install-python-imaging-in-a-virtualenv-with-no-site-packages/
    # """

    # no olvidar agregar mas adelante las relaciones solicitante(Solicitud) y votos(usuario)

    def __unicode__(self):
        """
        @param self: instancia del modelo de perfiles
        Necesario para poder visualizar, retorna en caracteres
        @return: self.usuario.username mediante la funcion __unicode__
        """

        return self.usuario.username