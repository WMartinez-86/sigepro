__author__ = 'juanma'

from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from apps.proyectos.models import Proyecto
from django.contrib.admin.widgets import FilteredSelectMultiple


ESTADOS = (

    ('PRO', 'Produccion'),
    ('APR', 'Aprobado'),
    ('FIN','Finalizado'),
    ('ELI','Eliminado'),
)


class ProyectoForm(ModelForm):
    #lider = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    #comite = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=True),
                                            #widget=FilteredSelectMultiple("Comite", is_stacked=False))

    class Meta:
        model = Proyecto
        exclude = ['estado','roles']



class CambiarEstadoForm(ModelForm):
    estado = forms.CharField(max_length=3, widget=forms.Select(choices=ESTADOS))

    class Meta:
        model = Proyecto
        exclude = ['nombre', 'descripcion', 'fecha_ini', 'fecha_fin', 'observaciones', 'nombreCorto', 'siglas', 'duracion_sprint']