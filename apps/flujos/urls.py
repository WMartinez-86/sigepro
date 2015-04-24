__author__ = 'juanma'


from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import registrar_flujo, listar_flujos
#from views import editar_fase,fases_todas, importar_fase, eliminar_fase, desasignar_usuario, desasociar,rol_proyecto,\
  #  crearol_proyecto,detallerol_proyecto, modificarrol_proyecto, eliminarrol_proyecto

urlpatterns = patterns('',
        #Administracion de Flujos

        url(r'^registrar/(?P<id_proyecto>\d+)$',registrar_flujo, name='registrar_flujos'),
        url(r'^proyecto/(?P<id_proyecto>\d+)$', listar_flujos, name='list_flujo'),
        )