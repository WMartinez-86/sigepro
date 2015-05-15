__author__ = 'juanma'

from django.forms import ModelForm
from django import forms
from apps.trabajos.models import Trabajo
from django.contrib.auth.models import Group


class TrabajoForm(ModelForm):
    class Meta:
        model = Trabajo
        exclude = ()

class CrearTrabajoForm(ModelForm):

    class Meta:
        model = Trabajo
        fields = ('nombre', 'descripcion', 'fInicio')

class ModificarTrabajoForm(ModelForm):
    class Meta:
        model = Trabajo
        fields = ('descripcion','fInicio')


class RolesForm(forms.Form):
    roles = forms.ModelMultipleChoiceField(queryset=Group.objects.none() )
    def __init__(self, flujo, *args, **kwargs):
        super(RolesForm, self).__init__(*args, **kwargs)
        self.fields['roles'].queryset = Group.objects.filter(flujo__id=flujo)