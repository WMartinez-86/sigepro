from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User, Permission
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from datetime import datetime

# Create your views here.
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from sigepro import settings
from apps.flujos.models import Flujo
from apps.userStories.models import UserStory
from apps.proyectos.models import Proyecto
from apps.userStories.forms import crearUserStoryForm
from django import forms
from django.core.mail import EmailMessage, send_mail
from apps.equipos.models import MiembroEquipo
from django.contrib.auth.models import User, Group



@login_required
def listar_userStories(request, id_proyecto):
    """
    vista para listar los userStories pertenecientes a la flujo
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_userStory: clave foranea a la flujo
    @return render_to_response(..) o HttpResponse(...)
    """
    rolSM = Group.objects.filter(name = "Scrum Master")
    equipi = MiembroEquipo.objects.filter(rol = rolSM, proyecto_id = id_proyecto)
    if equipi.count() == 0:
        mensaje = 101
        proyectos = Proyecto.objects.all()
        # proyecto = Proyecto.objects.get(id=id_proyecto)
        rolSM = Group.objects.filter(name = "Scrum Master")
        equipos = MiembroEquipo.objects.filter(rol = rolSM)
        return render_to_response('proyectos/listar_proyectos.html', {'proyectos': proyectos, 'equipos' : equipos, 'mensaje': mensaje}, context_instance=RequestContext(request))
    else:
        #tuserStory=get_object_or_404(Flujo,id=id_flujo)
        #flujo=Flujo.objects.filter(id=id_flujo)
        #if es_miembro(request.user.id,flujo,''):
        userStories=UserStory.objects.filter(proyecto_id = id_proyecto)
        #if puede_add_userStories(flujo):
        nivel = 3
        #id_proyecto=Flujo.objects.get().proyecto_id
        #proyecto=Proyecto.objects.get(pk=UserStory.proyecto)
        return render_to_response('userStories/listar_userStories.html', {'datos': userStories, 'id_proyecto': id_proyecto, 'nivel':nivel},
                                  context_instance=RequestContext(request))
        #else:
        #ESTE HAY QUE CORREGIR SI HAY TIEMPO
        #return HttpResponse("<h1>No se pueden administrar los UserStories de esta flujo. La flujo anterior aun no tiene userStories finalizados<h1>")

        #else:
        #return render_to_response('403.html')




@login_required

def crear_userStory(request, id_proyecto):
    """
    Vista para crear un user story. Ademas se dan las opciones de agregar un
    archivo al item, y de completar todos los atributos de su tipo de item
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_tipoItem: clave foranea al tipoItem
    @ return render_to_response('items/...) o render_to_response('403.html')
    """
    atri=1

    # print(cantidad_items(id_tipoItem))
    #id_fase=TipoItem.objects.get(id=id_tipoItem).fase_id
    #flag=es_miembro(request.user.id,id_fase,'add_item')


    #flujo=Flujo.objects.get(id=id_fase)
    #proyecto=flujo.proyecto_id
    #items=[]
    #tipoitem=[]
    #proyecto=Proyecto.objects.get(UserStory.proyecto)

    if request.method=='POST':
        #formset = ItemFormSet(request.POST)
        formulario = crearUserStoryForm(request.POST)

        if formulario.is_valid():
            today = datetime.now() #fecha actual
            dateFormat = today.strftime("%Y-%m-%d") # fecha con format
            #obtener item con el cual relacionar
            #item_nombre=request.POST.get('entradalista')

            newUserStory=UserStory(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],prioridad=request.POST['prioridad'],
                                   valor_negocio=request.POST['valor_negocio'],valor_tecnico=request.POST['valor_tecnico'],tiempo_estimado=request.POST['tiempo_estimado'],
                                   ultimo_cambio=datetime, proyecto_id=id_proyecto, flujo_id = None, estadoScrum=0)
            newUserStory.save()

            # enviar correo de notificacion al scrum master
            # proyecto = newUserStory.proyecto
            # id_proyecto = proyecto.id
            objdev = request.user
            desarrollador = User.get_full_name(objdev)
            rolSM = Group.objects.filter(name = "Scrum Master")
            equipi = MiembroEquipo.objects.get(rol = rolSM, proyecto_id = id_proyecto)
            SM = equipi.usuario
            correo = SM.email
            send_mail("Asunto", "Mensaje del sistema. \nEl usuario " + str(desarrollador) + " ha creado el siguiente User Story\n" +
                      "\nNombre: " + newUserStory.nombre +
                      "\nDescrpcion: " + newUserStory.descripcion +
                      "\nPrioridad: " + str(newUserStory.prioridad) +
                      "\nValor de negocio: " + str(newUserStory.valor_negocio) +
                      "\nValor tecnico: " + str(newUserStory.valor_tecnico) +
                      "\nTiempo estimado: " + str(newUserStory.tiempo_estimado) +
                      "\nUltimo cambio: " + str(newUserStory.ultimo_cambio) +
                      "\nEstado del Kanban: " + str(newUserStory.estadoKanban) +
                      "\nEstado del Scrum: " + str(newUserStory.estadoScrum),
                      '"SIGEPRO" <sigepro.is2@gmail.com>',[correo])


        return render_to_response('userStories/creacion_correcta.html',{'id_proyecto': id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = crearUserStoryForm()
        hijo=False
        #proyecto=Proyecto.objects.filter(id=flujo.proyecto_id)
        return render_to_response('userStories/crear_userStories.html', { 'formulario': formulario, 'id_proyecto': id_proyecto}, context_instance=RequestContext(request))




@login_required

def editar_userStory(request,id_userStory):
    '''
    vista para cambiar el nombre y la descripcion del tipo de item, y ademas agregar atributos al mismo
    Si el item se encuentra con el estado CON (solicitud de cambio aprobada), se puede modificar el item solo si el
    usuario es el que realizo la solicittud de cambio
    '''

    userStory_nuevo=get_object_or_404(UserStory,id=id_userStory)
    #fase=Fase.objects.get(id=item_nuevo.fase_id)
    #proyecto=Proyecto.objects.get(id=fase.proyecto_id)
    # #flag=es_miembro(request.user.id,item_nuevo.fase_id,'change_item')
    # atri=1
    # if flag==False:
    #     return HttpResponseRedirect('/denegado')

    #atributos=AtributoItem.objects.filter(id_item=id_item)
    # if len(atributos)==0:
    #     atri=0
    # if item_nuevo.estado=='CON':
    #     #archivos=Archivo.objects.filter(id_item=item_nuevo)
    #     #solicitudes=Solicitud.objects.filter(item=item_nuevo, estado='APROBADA')
    #     #solicitud=solicitudes[0]
    #     #solicitante=solicitud.usuario
    #
    #     if request.method=='POST':
    #         formulario = crearUserStoryForm(request.POST, instance=item_nuevo)
    #
    #         if formulario.is_valid():
    #
    #
    #             #generar_version(item_nuevo,request.user)
    #             today = datetime.now() #fecha actual
    #             dateFormat = today.strftime("%Y-%m-%d") # fecha con format
    #
    #             formulario.save()
    #             item_nuevo.fecha_mod=dateFormat
    #             #item_nuevo.version=item_nuevo.version+1
    #             item_nuevo.save()
    #
    #     else:
    #
    #         formulario = crearUserStoryForm(instance=item_nuevo)
    #         return render_to_response('userStory/modificar_item_solicitud.html', { 'formulario': formulario, 'item':item_nuevo}, context_instance=RequestContext(request))



    if request.method=='POST':

        formulario = crearUserStoryForm(request.POST, instance=userStory_nuevo)

        if formulario.is_valid():
            #generar_version(item_nuevo)
            today = datetime.now() #fecha actual
            dateFormat = today.strftime("%Y-%m-%d") # fecha con format

            formulario.save()
            userStory_nuevo.fecha_mod=dateFormat
            #userStory_nuevo.version=userStory_nuevo.version+1
            userStory_nuevo.save()

            # enviar correo de notificacion al scrum master
            objdev = request.user
            desarrollador = User.get_full_name(objdev)
            proyecto = userStory_nuevo.proyecto
            id_proyecto = proyecto.id
            rolSM = Group.objects.filter(name = "Scrum Master")
            equipi = MiembroEquipo.objects.get(rol = rolSM, proyecto_id = id_proyecto)
            # equipi = MiembroEquipo.objects.get(proyecto_id = id_proyecto)
            SM = equipi.usuario
            correo = SM.email
            #print str(userStory_nuevo.flujo.nombre)
            # print (correo)
            send_mail("Asunto", "Mensaje del sistema. \nEl usuario " + str(desarrollador) + " ha editado el siguiente User Story\n" +
                      "\nNombre: " + userStory_nuevo.nombre +
                      "\nDescrpcion: " + userStory_nuevo.descripcion +
                      "\nPrioridad: " + str(userStory_nuevo.prioridad) +
                      "\nValor de negocio: " + str(userStory_nuevo.valor_negocio) +
                      "\nValor tecnico: " + str(userStory_nuevo.valor_tecnico) +
                      "\nTiempo estimado: " + str(userStory_nuevo.tiempo_estimado) +
                      "\nUltimo cambio: " + str(userStory_nuevo.ultimo_cambio) +
                      "\nEstado del Kanban: " + str(userStory_nuevo.estadoKanban) +
                      "\nEstado del Scrum: " + str(userStory_nuevo.estadoScrum),
                      '"SIGEPRO" <sigepro.is2@gmail.com>',[correo])

            return render_to_response('userStories/creacion_correcta.html',{}, context_instance=RequestContext(request))

    else:

        formulario = crearUserStoryForm(instance=userStory_nuevo)
        #hijo=True
        return render_to_response('userStories/editar_userStory.html', { 'formulario': formulario}, context_instance=RequestContext(request))






@login_required
def detalle_userStory(request,id_userStory):
    """
    vista para ver los detalles del item <id_item>
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al item
    @return render_to_response(..)
    """
    #item=get_object_or_404(Item,id=id_item)
    #tipoitem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    #flujo=tipoitem.fase_id
    #fasse=Fase.objects.get(id=fase)
    #proyecto=Proyecto.objects.get(id=fasse.proyecto_id)

    #atributos=AtributoItem.objects.filter(id_item=id_item)
    #archivos=Archivo.objects.filter(id_item=id_item)
    dato = get_object_or_404(UserStory, pk=id_userStory)
    proyecto = Proyecto.objects.get(id = dato.proyecto_id)

    return render_to_response('userStories/detalle_userStory.html', {'datos': dato, 'proyecto': proyecto}, context_instance=RequestContext(request))

    #return render_to_response('403.html')




@login_required
def eliminar_userStory(request, id_userStory):
    """Funcion para Eliminar un rol.

   :param request: Parametro a ser procesado.
   :param pk: Parametro a ser procesado el identificador del rol que va a eliminarse.
   :type request: HttpRequest.
   :type pk: int.
   :returns: La pagina correspondiente.
   :rtype: El response correspondiente.
       """
    context = RequestContext(request)
    user_story = get_object_or_404(UserStory, id=id_userStory)
    if request.method == 'POST':
        user_story.delete()
        return redirect('listar_user_story')

    return render_to_response('adm/eliminar_user_story.html', {'object':user_story}, context)



def notificar(sender, instance, created, **kwargs):
    """
    Funcion que notifica al scrum master cuando se crea y se edita un user story

    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created:
        us = instance.UserStory




