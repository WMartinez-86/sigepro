__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import lista_proyectos
#from views import editar_proyecto, importar_proyecto, ver_equipo, cambiar_estado_proyecto

urlpatterns = patterns('',
        #url(r'^registrar/$',registrar_proyecto, name='registrar_proyecto'),
        #Administracion de Proyectos
        url(r'^$',lista_proyectos.as_view()),

        )
print urlpatterns