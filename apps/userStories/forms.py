__author__ = 'juanma'

from django import forms

from apps.userStories.models import UserStories
#from apps.solicitudes.models import Solicitud

ESTADOS = (

    ('PEN', 'Pendiente'),
 #   ('FIN','Finalizado'),
    ('VAL', 'Validado'),
)

class PrimeraUserStoriesForm(forms.ModelForm):
    class Meta:
        model= UserStories
        exclude=('estado', 'version', 'relacion', 'fecha_creacion', 'fecha_mod','tipo', 'tipo_item','fase','lineaBase')

class EstadoUserStoriesForm(forms.ModelForm):
    estado=forms.CharField(max_length=3,widget=forms.Select(choices= ESTADOS))
    class Meta:
        model=UserStories
        fields=['estado']


# class SolicitudCambioForm(forms.ModelForm):
#     class Meta:
#         model=Solicitud