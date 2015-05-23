__author__ = 'juanma'

from django import forms
from apps.equipos.models import MiembroEquipo


class crearEquipoForm(forms.ModelForm):
    class Meta:
        model= MiembroEquipo
        fields = ('usuario','proyecto','rol','horasPorDia')