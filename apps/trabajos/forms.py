__author__ = 'juanma'

from django import forms

from apps.trabajos.models import Trabajo
#from apps.solicitudes.models import Solicitud

ESTADOS = (

    ('PEN', 'Pendiente'),
 #   ('FIN','Finalizado'),
    ('VAL', 'Validado'),
)

class crearTrabajoForm(forms.ModelForm):
    class Meta:
        model= Trabajo
        #exclude = ('fecha',)
        fields = ['descripcion','userstory','sprint','tipo_trabajo']

# class EstadoTrabajoForm(forms.ModelForm):
#     estado=forms.CharField(max_length=3,widget=forms.Select(choices= ESTADOS))
#     class Meta:
#         model=Trabajo
#         fields=['estado']


