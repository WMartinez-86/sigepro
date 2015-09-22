__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()

from .views import hello_pdf, generar_pdf

urlpatterns = patterns('',
    url(r'^$', generar_pdf, name='hello_pdf'),
    # url(r'^$',lista_roles,name='lista_roles'),
    # url(r'^(?P<id_rol>\d+)$', detalle_rol, name='detalle_rol'),
    # url(r'^eliminar/(?P<id_rol>\d+)$', eliminar_rol, name='eliminar_rol'),
    # url(r'^modificar/(?P<id_rol>\d+)$', editar_rol, name='editar_rol'),
    # url(r'^search/$',buscarRol, name='buscar_roles'),
    # url(r'^register/success/$',RegisterSuccessView.as_view()),
    #url(r'^$', lista_roles.as_view()),
    )
print urlpatterns