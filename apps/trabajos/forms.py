__author__ = 'juanma'

from django import forms

from apps.trabajos.models import Trabajo, Adjunto
#from apps.solicitudes.models import Solicitud


class crearTrabajoForm(forms.ModelForm):
    class Meta:
        model= Trabajo
        # exclude = ()
        fields = ['fecha', 'descripcion', 'hora']

# class EstadoTrabajoForm(forms.ModelForm):
#     estado=forms.CharField(max_length=3,widget=forms.Select(choices= ESTADOS))
#     class Meta:
#         model=Trabajo
#         fields=['estado']

class NuevoAdjunto(forms.ModelForm):
    class Meta:
        model= Adjunto
#        fields=['nombre', 'descripcion']
        exclude = ('trabajo', 'creacion')


