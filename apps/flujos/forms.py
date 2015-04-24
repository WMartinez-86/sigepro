__author__ = 'juanma'


from django.forms import ModelForm
from django import forms
from apps.flujos.models import Flujo
from django.contrib.auth.models import Group


class FlujoForm(ModelForm):
    class Meta:
        model = Flujo

class CrearFlujoForm(ModelForm):

    class Meta:
        model = Flujo
        #fields = ('nombre')

class ModificarFlujoForm(ModelForm):
    class Meta:
        model = Flujo
        #fields = ('nombre')


class RolesForm(forms.Form):
    roles = forms.ModelMultipleChoiceField(queryset=Group.objects.none() )
    def __init__(self, fase, *args, **kwargs):
        super(RolesForm, self).__init__(*args, **kwargs)
        self.fields['roles'].queryset = Group.objects.filter(fase__id=fase)