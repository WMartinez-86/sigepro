#from django.shortcuts import render
from django.views.generic import ListView

from .models import Rol

# Create your views here.

class RolesView(ListView): # ListView importa todos los objetos de un modelo
    template_name = 'listar_roles.html'
    model = Rol
