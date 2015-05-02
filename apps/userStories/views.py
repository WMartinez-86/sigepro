from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User, Permission
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from datetime import datetime

# Create your views here.
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from sigepro import settings
from apps.flujos.models import Flujo
from apps.userStories.models import UserStory, Archivo
from apps.proyectos.models import Proyecto
from apps.userStories.forms import crearUserStoryForm
from django import forms



@login_required
def listar_userStories(request):
    """
    vista para listar los userStories pertenecientes a la flujo
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_userStory: clave foranea a la flujo
    @return render_to_response(..) o HttpResponse(...)
    """
    #tuserStory=get_object_or_404(Flujo,id=id_flujo)
    #flujo=Flujo.objects.filter(id=id_flujo)
    #if es_miembro(request.user.id,flujo,''):
    userStories=UserStory.objects.filter()
    #if puede_add_userStories(flujo):
    nivel = 3
    #id_proyecto=Flujo.objects.get().proyecto_id
    #proyecto=Proyecto.objects.get()
    return render_to_response('userStories/listar_userStories.html', {'datos': userStories, 'nivel':nivel},
                                  context_instance=RequestContext(request))
    #else:
        #ESTE HAY QUE CORREGIR SI HAY TIEMPO
        #return HttpResponse("<h1>No se pueden administrar los UserStories de esta flujo. La flujo anterior aun no tiene userStories finalizados<h1>")

    #else:
    #return render_to_response('403.html')





# @login_required
# def detalle_userStory(request, id_userStory):
#     """
#     vista para ver los detalles del userStory <id_userStory>
#     @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
#     @param id_userStory: clave foranea al userStory
#     @return render_to_response(..)
#     """
#     userStory=get_object_or_404(UserStory,id=id_userStory)
#     tipouserStory=get_object_or_404(TipoUserStory,id=userStory.tipo_userStory_id)
#     flujo=tipouserStory.flujo_id
#     fasse=Flujo.objects.get(id=flujo)
#     proyecto=Proyecto.objects.get(id=fasse.proyecto_id)
#     if es_miembro(request.user.id, flujo,''):
#         atributos=AtributoUserStory.objects.filter(id_userStory=id_userStory)
#         archivos=Archivo.objects.filter(id_userStory=id_userStory)
#         dato = get_object_or_404(UserStory, pk=id_userStory)
#
#         return render_to_response('userStories/detalle_userStory.html', {'datos': dato, 'atributos': atributos, 'archivos':archivos,'flujo':fasse,'proyecto':proyecto}, context_instance=RequestContext(request))
#     else:
#         return render_to_response('403.html')




@login_required

def crear_userStory(request):
    """
      Vista para crear un item y asignarlo a un tipo de item. Ademas se dan las opciones de agregar un
    archivo al item, y de completar todos los atributos de su tipo de item
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_tipoItem: clave foranea al tipoItem
    @ return render_to_response('items/...) o render_to_response('403.html')
    """
    atri=1

    # print(cantidad_items(id_tipoItem))

    items=[]


    if request.method=='POST':
        #formset = ItemFormSet(request.POST)
        formulario = crearUserStoryForm(request.POST)

        if formulario.is_valid():
            today = datetime.now() #fecha actual
            dateFormat = today.strftime("%Y-%m-%d") # fecha con format
            return render_to_response('userStories/crear_userStories.html', { 'formulario': formulario},
                                      context_instance=RequestContext(request))


            cod=newUserStory=UserStory(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1,fecha_creacion=dateFormat, fecha_mod=dateFormat)
            newUserStory.save()


            #guardar archivo
        if request.FILES.get('file')!=None:
            archivo=Archivo(archivo=request.FILES['file'],nombre='', id_item_id=cod.id)
            archivo.save()

            #guardar atributos

            return render_to_response('userStories/creacion_correcta.html', context_instance=RequestContext(request))
    else:

        formulario = crearUserStoryForm()
        hijo=False
        #proyecto=Proyecto.objects.filter(id=flujo.proyecto_id)
        #return render_to_response('userStories/crear_userStories.html', { 'formulario': formulario, 'hijo':hijo,'atri':atri}, context_instance=RequestContext(request))


