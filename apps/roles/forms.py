__author__ = 'smgalu'

from django import forms
from apps.roles.models import Rol
from django.contrib.auth.models import Group, Permission


class GroupForm(forms.ModelForm):
    # permissions = Group.objects.exclude(permission_id=1,permission_id=2,permission_id=3)
    class Meta:
        model = Group
        # fields=['nombre']
