__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import lista_proyectos, registra_proyecto, RegisterSuccessView, editar_proyecto, buscar_proyecto, detalle_proyecto
from views import proyecto_iniciar
from apps.equipos.views import ver_equipo

urlpatterns = patterns('',
        #url(r'^registrar/$',registra_proyecto.as_view()),
        url(r'^registrar/$',registra_proyecto, name='registrar_proyectos'),
        #Administracion de Proyectos
        url(r'^$',lista_proyectos, name='listar_proyectos'),
        url(r'^register/success/$',RegisterSuccessView ,name='RegisterSuccessView'),
        url(r'^modificar/(?P<id_proyecto>\d+)$', editar_proyecto, name='edit_proyecto'),
        url(r'^search/$',buscar_proyecto, name='buscar_proyectos'),
        # url(r'^cambiarEstado/(?P<id_proyecto>\d+)$', cambiar_estado_proyecto, name='camb_est_proyect'),
        url(r'^(?P<id_proyecto>\d+)$', detalle_proyecto, name='detalle_proyecto'),
        #url(r'^equipo/(?P<id_proyecto>\d+)$', ver_equipo, name='equipo'),
        # cambios de estado
        url(r'^iniciar/(?P<id_proyecto>\d+)$', proyecto_iniciar, name='proyecto_iniciar'),
        )
print urlpatterns