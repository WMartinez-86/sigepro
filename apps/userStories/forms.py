__author__ = 'juanma'

from django import forms

from apps.userStories.models import UserStory

ESTADOS = (

    ('PEN', 'Pendiente'),
 #   ('FIN','Finalizado'),
    ('VAL', 'Validado'),
)

class PrimerFlujoForm(forms.ModelForm):
    class Meta:
        model= UserStory
        exclude=('estado', 'fecha_creacion', 'fecha_mod', 'flujo')

class EstadoUSForm(forms.ModelForm):
    estado=forms.CharField(max_length=3,widget=forms.Select(choices= ESTADOS))
    class Meta:
        model=UserStory
        fields=['estado']