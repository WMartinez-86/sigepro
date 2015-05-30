__author__ = 'juanma'


from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_sprints, registrar_sprint, eliminar_sprint, buscar_sprints, iniciar_sprint, finalizar_sprint, graficar
#from views import editar_sprint,sprints_todas, importar_sprint, desasignar_usuario

urlpatterns = patterns('',
        #Administracion de Sprints
        url(r'^registrar/(?P<id_proyecto>\d+)$',registrar_sprint, name='registrar_sprints'),
        url(r'^proyecto/(?P<id_proyecto>\d+)$', listar_sprints, name='list_sprint'),
        #url(r'^editar/(?P<id_sprint>\d+)$', editar_sprint, name='edit_sprint'),
        #url(r'^lista_todas/(?P<id_proyecto>\d+)$',sprints_todas,name='sprints_todas'),
        #url(r'^importar/(?P<id_sprint>\d+)-(?P<id_proyecto>\d+)$', importar_sprint,name='importar_sprint'),
        #url(r'^(?P<id_sprint>\d+)$', detalle_sprint, name='detalle_sprint'),
        url(r'^eliminar/(?P<id_sprint>\d+)$', eliminar_sprint, name='eliminar_sprint'),
        url(r'^iniciar/(?P<id_sprint>\d+)$', iniciar_sprint, name='iniciar_sprint'),
        url(r'^finalizar/(?P<id_sprint>\d+)$', finalizar_sprint, name='finalizar_sprint'),
        url(r'^search/(?P<id_proyecto>\d+)$',buscar_sprints, name='buscar_sprints'),
        url(r'^graficar/(?P<id_sprint>\d+)$',graficar, name='graficar'),
        #url(r'^roles/(?P<id_sprint>\d+)$', rol_proyecto, name='rol_proyecto'),
        #url(r'^roles/crear/(?P<id_sprint>\d+)$', crearol_proyecto, name='crearol_proyecto'),
        #url(r'^roles/detalle/(?P<id_rol>\d+)-(?P<id_sprint>\d+)$', detallerol_proyecto, name='detallerol_proyecto'),
        #url(r'^roles/modificar/(?P<id_rol>\d+)-(?P<id_sprint>\d+)$', modificarrol_proyecto, name='modificarrol_proyecto'),
        #url(r'^roles/eliminar/(?P<id_rol>\d+)-(?P<id_sprint>\d+)$', eliminarrol_proyecto, name='eliminarrol_proyecto'),
        #url(r'^asignar/(?P<id_sprint>\d+)$', asignar_usuario, name='asignar_usuario'),
        #url(r'^asignar/(?P<id_usuario>\d+)/(?P<id_sprint>\d+)$', asignar_rol, name='asignar_rol'),
        #url(r'^asociar/(?P<id_rol>\d+)-(?P<id_usuario>\d+)-(?P<id_sprint>\d+)$', asociar,name='asociar'),
        #url(r'^desasignar/(?P<id_sprint>\d+)$', desasignar_usuario, name='des'),
        #url(r'^desasignar/(?P<id_usuario>\d+)/(?P<id_sprint>\d+)$', desasociar,name='desasociar'),
        )