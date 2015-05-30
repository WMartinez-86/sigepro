__author__ = 'juanma'


from django.forms import ModelForm
from django import forms
from apps.sprints.models import Sprint
from apps.flujos.models import Flujo
from apps.userStories.models import UserStory
from django.contrib.auth.models import Group, User


class SprintForm(ModelForm):
    class Meta:
        model = Sprint
        exclude = ()

class CrearSprintForm(ModelForm):
    class Meta:
        model = Sprint
        fields = ('nombre', 'descripcion', 'inicio_propuesto', 'fin_propuesto')

class AsignarFlujoDesarrollador(ModelForm):
    class Meta:
    #desarrollador = forms.ModelChoiceField(queryset=User.objects.filter(Miembro))
    #flujo = forms.ModelChoiceField(queryset=Flujo.objects.filter(id= 1))
    #def __init__(self, id_, *args, **kwargs):
        model = UserStory
        fields = ('flujo', 'desarrollador')


class RolesForm(forms.Form):
    roles = forms.ModelMultipleChoiceField(queryset=Group.objects.none())
    def __init__(self, sprint, *args, **kwargs):
        super(RolesForm, self).__init__(*args, **kwargs)
        self.fields['roles'].queryset = Group.objects.filter(sprint__id=sprint)