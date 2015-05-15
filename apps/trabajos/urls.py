__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
from apps.trabajos.views import listar_trabajos

admin.autodiscover()


urlpatterns = patterns('',

                       #url(r'^crear/$',crear_userStory, name='crear_userStories'),
                       url(r'^userStories/(?P<id_userStory>\d+)$', listar_trabajos, name='listar_trabajos'),
                       #url(r'^detalle/(?P<id_userStory>\d+)$',detalle_userStory, name='detalle_userStory'),
                       #url(r'^modificar/(?P<id_userStory>\d+)$',editar_userStory, name='editar_userStory'),
                       #url(r'^eliminar/(?P<id_userStory>\d+)$',eliminar_userStory,name='eliminar_userStory'),

                       )