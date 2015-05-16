__author__ = 'juanma'


from django.forms import ModelForm
from django import forms
from apps.actividades.models import Actividad
from django.contrib.auth.models import Group


class ActividadForm(ModelForm):
    class Meta:
        model = Actividad
        exclude = ()

class CrearActividadForm(ModelForm):

    class Meta:
        model = Actividad
        fields = ('nombre',)

class ModificarActividadForm(ModelForm):
    class Meta:
        model = Actividad
        fields = ('nombre',)
