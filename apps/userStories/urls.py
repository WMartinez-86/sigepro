__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
from apps.userStories.views import listar_proyectos,listar_userStories, crear_userStories, listar_flujos
#from apps.userStories.views import editar_item, eliminar_archivo,detalle_tiposDeItem, seleccion_tipoItem, crear_item_hijo,cambiar_estado_item
#from apps.userStories.views import listar_archivos, detalle_version_item, listar_versiones, reversionar_item,descargo_archivo, cambiar_padre,\
#    cambiar_antecesor,grafo_relaciones,eliminar_item,listar_muertos,revivir
admin.autodiscover()


urlpatterns = patterns('',
        url(r'^proyectos/$',listar_proyectos, name='listar_proyectos'),
        url(r'^proyectos/flujos/(?P<id_proyecto>\d+)$',listar_flujos, name='listar_flujos'),
        #url(r'^flujos/tiposDeItem/(?P<id_fase>\d+)$',listar_tiposDeItem, name='listar_tiposDeItem'),
        #url(r'^flujos/tiposDeItem/detalle/(?P<id_tipoItem>\d+)$',detalle_tiposDeItem, name='detalle_tiposDeItem'),
        #url(r'^userStories/selectTipoItem/(?P<id_fase>\d+)$',seleccion_tipoItem, name='seleccion_tipoItem'),
        url(r'^userStories/crear/(?P<id_tipoItem>\d+)$',crear_userStories, name='crear_item'),
        url(r'^userStories/listar/(?P<id_flujo>\d+)$',listar_userStories, name='listar_userStories'),
        #url(r'^userStories/detalle/(?P<id_item>\d+)$',detalle_item, name='detalle_item'),

        )