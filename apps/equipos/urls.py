__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
from views import ver_equipo, agregar_miembro

admin.autodiscover()


urlpatterns = patterns('',

                       url(r'^(?P<id_proyecto>\d+)$',ver_equipo, name='ver_equipo'),
                       url(r'^agregar/(?P<id_proyecto>\d+)$',agregar_miembro, name='agregar_miembro'),


                       )