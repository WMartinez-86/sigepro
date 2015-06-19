__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
from apps.userStories.views import listar_userStories, crear_userStory, detalle_userStory, editar_userStory, eliminar_userStory
# from apps.userStories.views import sprintF_USNoTerminados
from apps.trabajos.views import listar_trabajos

admin.autodiscover()


urlpatterns = patterns('',

                       url(r'^crear/(?P<id_proyecto>\d+)$',crear_userStory, name='crear_userStories'),
                       url(r'^(?P<id_proyecto>\d+)$',listar_userStories, name='listar_userStories'),
                       url(r'^detalle/(?P<id_userStory>\d+)$',detalle_userStory, name='detalle_userStory'),
                       url(r'^modificar/(?P<id_userStory>\d+)$',editar_userStory, name='editar_userStory'),
                       url(r'^eliminar/(?P<id_userStory>\d+)$',eliminar_userStory,name='eliminar_userStory'),
                       url(r'^eliminar/(?P<id_userStory>\d+)$',eliminar_userStory,name='eliminar_userStory'),
                       url(r'^trabajos/(?P<id_userStory>\d+)$', listar_trabajos, name='listar_trabajos'),
                       # url(r'^USNoFinalizados/(?P<id_userStory>\d+)$', sprintF_USNoTerminados, name='Listar_USNoFinalizados'),



                       )

