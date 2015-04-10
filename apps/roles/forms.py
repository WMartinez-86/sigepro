__author__ = 'smgalu'

from django import forms

from django.contrib.auth.models import Group, Permission


class GroupForm(forms.ModelForm):
    permissions = Group.objects.exclude(id=1)
    class Meta:
        model = Group
        fields=['name','permissions']

