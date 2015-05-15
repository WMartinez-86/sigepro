from django.contrib import admin
from apps.trabajos.models import Trabajo, Archivo

# Register your models here.
admin.site.register(Trabajo)
admin.site.register(Archivo)