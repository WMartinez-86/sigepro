__author__ = 'juanma'

from django import forms

from apps.userStories.models import UserStory
#from apps.solicitudes.models import Solicitud

ESTADOS = (

    ('PEN', 'Pendiente'),
 #   ('FIN','Finalizado'),
    ('VAL', 'Validado'),
)

class crearUserStoryForm(forms.ModelForm):
    class Meta:
        model= UserStory
        exclude = ('actividad', 'flujo', 'estadoKanban', 'estadoScrum', 'proyecto', 'desarrollador', 'sprint', 'version', 'orden', 'fecha_mod')

class EstadoUserStoryForm(forms.ModelForm):
    estado=forms.CharField(max_length=3,widget=forms.Select(choices= ESTADOS))
    class Meta:
        model=UserStory
        fields=['estado']


# class SolicitudCambioForm(forms.ModelForm):
#     class Meta:
#         model=Solicitud
#         fields=['nombre', 'descripcion']