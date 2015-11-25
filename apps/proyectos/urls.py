__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import lista_proyectos, registra_proyecto, RegisterSuccessView, editar_proyecto, buscar_proyecto, detalle_proyecto
from views import proyecto_iniciar, proyecto_finalizar, proyecto_aprobar, proyecto_eliminar, proyecto_rechazar, listar_reportes, generar_pdf
from views import reporte_horas_trabajos, reporte_trabajos_dev, reporte_trabajos_rest, reporte_grafica

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
        url(r'^finalizar/(?P<id_proyecto>\d+)$', proyecto_finalizar, name='proyecto_iniciar'),
        url(r'^aprobar/(?P<id_proyecto>\d+)$', proyecto_aprobar, name='proyecto_iniciar'),
        url(r'^eliminar/(?P<id_proyecto>\d+)$', proyecto_eliminar, name='proyecto_iniciar'),
        url(r'^rechazar/(?P<id_proyecto>\d+)$', proyecto_rechazar, name='proyecto_iniciar'),
        url(r'^listar_reportes/(?P<id_proyecto>\d+)$',listar_reportes , name='listar_pdf'),
        url(r'^listar_reportes/generar/(?P<id_proyecto>\d+)$', reporte_horas_trabajos , name='pdf'),
        url(r'^listar_reportes/generar2/(?P<id_proyecto>\d+)$', reporte_trabajos_dev , name='pdf'),
        url(r'^listar_reportes/generar3/(?P<id_proyecto>\d+)$', reporte_trabajos_rest , name='pdf'),
        url(r'^listar_reportes/generar4/(?P<id_proyecto>\d+)$', reporte_grafica , name='pdf'),
        )
print urlpatterns
