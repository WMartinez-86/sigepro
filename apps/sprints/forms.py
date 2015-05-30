__author__ = 'juanma'


from django.forms import ModelForm
from django import forms
from apps.sprints.models import Sprint
from django.contrib.auth.models import Group


class SprintForm(ModelForm):
    class Meta:
        model = Sprint
        exclude = ()

class CrearSprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = ('nombre', 'descripcion')

class RolesForm(forms.Form):
    roles = forms.ModelMultipleChoiceField(queryset=Group.objects.none() )
    def __init__(self, sprint, *args, **kwargs):
        super(RolesForm, self).__init__(*args, **kwargs)
        self.fields['roles'].queryset = Group.objects.filter(sprint__id=sprint)