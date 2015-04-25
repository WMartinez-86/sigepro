__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
from apps.userStories.views import crear_userStory, listar_userStories, detalle_userStory
from apps.userStories.views import editar_userStory, eliminar_archivo, cambiar_estado_userStory
from apps.userStories.views import listar_archivos, descargo_archivo, eliminar_userStory

admin.autodiscover()


urlpatterns = patterns('',

                       url(r'^userStory/crear/(?P<id_tipoItem>\d+)$',crear_userStory, name='crear_userStory'),
                       url(r'^userStory/listar/(?P<id_fase>\d+)$',listar_userStories, name='listar_userStories'),
                       url(r'^userStory/detalle/(?P<id_userStory>\d+)$',detalle_userStory, name='detalle_userStory'),
                       url(r'^userStory/modificar/(?P<id_userStory>\d+)$',editar_userStory, name='editar_userStory'),

                       url(r'^userStory/archivos/(?P<id_userStory>\d+)$',listar_archivos, name='listar_archivos'),
                       url(r'^userStory/descargar/(?P<idarchivo>\d+)$',descargo_archivo, name='descargar_archivos'),
                       url(r'^userStory/archivos/eliminar/(?P<id_archivo>\d+)$',eliminar_archivo,name='eliminar_archivo'),
                       url(r'^userStory/cambiar_estado/(?P<id_userStory>\d+)$',cambiar_estado_userStory,name='cambiar_estado'),

                       url(r'^userStory/eliminar_userStory/(?P<id_userStory>\d+)$',eliminar_userStory,name='eliminar_userStory'),

                       )