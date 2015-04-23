__author__ = 'smgalu'

from django import forms

from django.contrib.auth.models import Group, Permission
from .models import Rol


class GroupForm(forms.ModelForm):
    #permission = Group.objects.exclude(id=1)
    class Meta:
        model = Group
        fields=['name','permissions']
#
# class RolForm(forms.ModelForm):
#     class Meta:
#         model = Rol
#         exclude = ['id']