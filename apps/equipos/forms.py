__author__ = 'juanma'

from django import forms
from apps.equipos.models import MiembroEquipo
from django.contrib.auth.models import User


class crearEquipoForm(forms.ModelForm):
    class Meta:
        model= MiembroEquipo
        fields = ('usuario','rol','horasPorDia')

        def __init__(self, filter, *args, **kwargs):
		super(crearEquipoForm, self).__init__(*args, **kwargs)
		self.fields['User'].query_set = User.objects.filter(filter)