__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import lista_proyectos, registra_proyecto
#from views import editar_proyecto, importar_proyecto, ver_equipo, cambiar_estado_proyecto

urlpatterns = patterns('',
        #url(r'^registrar/$',registra_proyecto.as_view()),
        url(r'^registrar/$',registra_proyecto, name='registrar_proyectos'),
        #Administracion de Proyectos
        url(r'^$',lista_proyectos.as_view()),

        )
print urlpatterns