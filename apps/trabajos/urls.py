__author__ = 'juanma'

from django.conf.urls import patterns, url
from django.contrib import admin
from apps.trabajos.views import listar_trabajos, crear_trabajo, upload_handler, upload_listar, download_attachment

admin.autodiscover()


urlpatterns = patterns('',

                       url(r'^crear/(?P<id_userStory>\d+)$',crear_trabajo, name='crear_trabajo'),
                       url(r'^userStories/(?P<id_userStory>\d+)$', listar_trabajos, name='listar_trabajos'),
                       #url(r'^detalle/(?P<id_userStory>\d+)$',detalle_userStory, name='detalle_userStory'),
                       #url(r'^modificar/(?P<id_userStory>\d+)$',editar_userStory, name='editar_userStory'),
                       #url(r'^eliminar/(?P<id_userStory>\d+)$',eliminar_userStory,name='eliminar_userStory'),
                       #url(r'^attachment/(?P<pk>\d+)/$',upload_handler , name='download_attachment'),
                        #url(r'^file/(?P<pk>\d+)/$', views.FileDetail.as_view(), name="file_detail"),
                       #url(r'^nota/(?P<pk>\d+)/$', views.NotaDetail.as_view(), name='nota_detail'),
                       #url(r'^userstory/(?P<pk>\d+)/notas/$', views.NotaList.as_view(), name="nota_list"),
                       #url(r'^userstory/(?P<pk>\d+)/files/$', views.FileList.as_view(), name="file_list"),
                       url(r'^adjuntar/(?P<id_trabajo>\d+)$', upload_listar, name='upload_listar'),
                       url(r'^attachment/(?P<pk>\d+)/$', download_attachment, name='download_attachment'),


)