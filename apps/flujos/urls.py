__author__ = 'juanma'


from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_flujos, registrar_flujo, detalle_flujo, buscar_flujos, asignar_rol, asignar_usuario, asociar
from views import editar_flujo,flujos_todas, importar_flujo, eliminar_flujo, desasignar_usuario, desasociar,rol_proyecto,\
    crearol_proyecto,detallerol_proyecto, modificarrol_proyecto, eliminarrol_proyecto

urlpatterns = patterns('',
        #Administracion de Flujos
        url(r'^registrar/(?P<id_proyecto>\d+)$',registrar_flujo, name='registrar_flujos'),
        url(r'^proyecto/(?P<id_proyecto>\d+)$', listar_flujos, name='list_flujo'),
        url(r'^editar/(?P<id_flujo>\d+)$', editar_flujo, name='edit_flujo'),
        url(r'^lista_todas/(?P<id_proyecto>\d+)$',flujos_todas,name='flujos_todas'),
        url(r'^importar/(?P<id_flujo>\d+)-(?P<id_proyecto>\d+)$', importar_flujo,name='importar_flujo'),
        url(r'^(?P<id_flujo>\d+)$', detalle_flujo, name='detalle_flujo'),
        url(r'^eliminar/(?P<id_flujo>\d+)$', eliminar_flujo, name='eliminar_flujo'),
        url(r'^search/(?P<id_proyecto>\d+)$',buscar_flujos, name='buscar_flujos'),
        #url(r'^roles/(?P<id_flujo>\d+)$', rol_proyecto, name='rol_proyecto'),
        #url(r'^roles/crear/(?P<id_flujo>\d+)$', crearol_proyecto, name='crearol_proyecto'),
        #url(r'^roles/detalle/(?P<id_rol>\d+)-(?P<id_flujo>\d+)$', detallerol_proyecto, name='detallerol_proyecto'),
        #url(r'^roles/modificar/(?P<id_rol>\d+)-(?P<id_flujo>\d+)$', modificarrol_proyecto, name='modificarrol_proyecto'),
        #url(r'^roles/eliminar/(?P<id_rol>\d+)-(?P<id_flujo>\d+)$', eliminarrol_proyecto, name='eliminarrol_proyecto'),
        #url(r'^asignar/(?P<id_flujo>\d+)$', asignar_usuario, name='asignar_usuario'),
        #url(r'^asignar/(?P<id_usuario>\d+)/(?P<id_flujo>\d+)$', asignar_rol, name='asignar_rol'),
        #url(r'^asociar/(?P<id_rol>\d+)-(?P<id_usuario>\d+)-(?P<id_flujo>\d+)$', asociar,name='asociar'),
        #url(r'^desasignar/(?P<id_flujo>\d+)$', desasignar_usuario, name='des'),
        #url(r'^desasignar/(?P<id_usuario>\d+)/(?P<id_flujo>\d+)$', desasociar,name='desasociar'),
        )