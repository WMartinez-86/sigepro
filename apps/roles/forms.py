__author__ = 'smgalu'

from django import forms

class RolCrear(forms.Form):
    nombre = forms.CharField(max_length=50)