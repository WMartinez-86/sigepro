__author__ = 'juanma'


from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_actividades, registrar_actividad, detalle_actividad, buscar_actividades,estadoKanban, asignar_usuario
from views import editar_actividad,actividades_todas, eliminar_actividad, desasignar_usuario

urlpatterns = patterns('',
        #Administracion de Actividades
        url(r'^registrar/(?P<id_flujo>\d+)$',registrar_actividad, name='registrar_actividades'),
        url(r'^flujo/(?P<id_flujo>\d+)$', listar_actividades, name='list_actividad'),
        url(r'^editar/(?P<id_actividad>\d+)$', editar_actividad, name='edit_actividad'),
        url(r'^lista_todas/(?P<id_flujo>\d+)$',actividades_todas,name='actividades_todas'),
        url(r'^(?P<id_actividad>\d+)$', detalle_actividad, name='detalle_actividad'),
        url(r'^eliminar/(?P<id_actividad>\d+)$', eliminar_actividad, name='eliminar_actividad'),
        url(r'^search/(?P<id_flujo>\d+)$',buscar_actividades, name='buscar_actividades'),
        url(r'^kanban/(?P<id_actividad>\d+)$', estadoKanban, name='estadoKanban'),

        )