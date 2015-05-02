__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
from apps.userStories.views import listar_userStories, crear_userStory

admin.autodiscover()


urlpatterns = patterns('',

                       url(r'^crear/$',crear_userStory, name='crear_userStories'),
                       url(r'^$',listar_userStories, name='listar_userStories'),
                       #url(r'^userStory/detalle/(?P<id_userStory>\d+)$',detalle_userStory, name='detalle_userStory'),
                       #url(r'^userStory/modificar/(?P<id_userStory>\d+)$',editar_userStory, name='editar_userStory'),


                       )

