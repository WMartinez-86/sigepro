from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sigepro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #INICIO
    url(r'^$', include('apps.inicio.urls')),
    #USUARIOS
    url(r'^usuarios/',include('apps.usuarios.urls')),
    #ROLES
    url(r'^roles/',include('apps.roles.urls')),
    #PROYECTOS
    url(r'^proyectos/',include('apps.proyectos.urls')),


)
