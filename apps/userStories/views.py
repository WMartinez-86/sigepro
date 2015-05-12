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
from apps.userStories.models import UserStory
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
    #proyecto=Proyecto.objects.get(pk=UserStory.proyecto)
    return render_to_response('userStories/listar_userStories.html', {'datos': userStories, 'nivel':nivel},
                                  context_instance=RequestContext(request))
    #else:
        #ESTE HAY QUE CORREGIR SI HAY TIEMPO
        #return HttpResponse("<h1>No se pueden administrar los UserStories de esta flujo. La flujo anterior aun no tiene userStories finalizados<h1>")

    #else:
    #return render_to_response('403.html')




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
                                       tiempo_registrado=request.POST['tiempo_registrado'], ultimo_cambio=datetime)
            newUserStory.save()
            #guardar archivo

            #guardar atributos
        return render_to_response('userStories/creacion_correcta.html',{}, context_instance=RequestContext(request))
    else:

        formulario = crearUserStoryForm()
        hijo=False
        #proyecto=Proyecto.objects.filter(id=flujo.proyecto_id)
        return render_to_response('userStories/crear_userStories.html', { 'formulario': formulario}, context_instance=RequestContext(request))






def editar_userStory(request):
    '''
    vista para cambiar el nombre y la descripcion del tipo de item, y ademas agregar atributos al mismo
    Si el item se encuentra con el estado CON (solicitud de cambio aprobada), se puede modificar el item solo si el
    usuario es el que realizo la solicittud de cambio
    '''

    item_nuevo=get_object_or_404(Item,id=id_item)
    fase=Fase.objects.get(id=item_nuevo.fase_id)
    proyecto=Proyecto.objects.get(id=fase.proyecto_id)
    flag=es_miembro(request.user.id,item_nuevo.fase_id,'change_item')
    atri=1
    if flag==False:
        return HttpResponseRedirect('/denegado')

    atributos=AtributoItem.objects.filter(id_item=id_item)
    if len(atributos)==0:
        atri=0
    if item_nuevo.estado=='CON':
        archivos=Archivo.objects.filter(id_item=item_nuevo)
        solicitudes=Solicitud.objects.filter(item=item_nuevo, estado='APROBADA')
        solicitud=solicitudes[0]
        solicitante=solicitud.usuario
        if request.user==solicitante:
            if request.method=='POST':
                formulario = PrimeraFaseForm(request.POST, instance=item_nuevo)

                if formulario.is_valid():

                    if request.FILES.get('file')!=None:
                        archivo=Archivo(archivo=request.FILES['file'],nombre='', id_item_id=id_item)
                        archivo.save()
                    #generar_version(item_nuevo,request.user)
                    today = datetime.now() #fecha actual
                    dateFormat = today.strftime("%Y-%m-%d") # fecha con format

                    formulario.save()
                    item_nuevo.fecha_mod=dateFormat
                    #item_nuevo.version=item_nuevo.version+1
                    item_nuevo.save()

                    for atributo in atributos:

                        a=request.POST[atributo.id_atributo.nombre]
                        if a!=None:
                            #validar atributos antes de guardarlos
                            validar=True
                            if atributo.id_atributo.tipo == "FEC":
                                try:
                                    fecha = datetime.strptime(str(a), '%d/%m/%Y')
                                except ValueError:
                                    validar=False
                            else:
                                if atributo.id_atributo.tipo == "NUM":
                                    a = a.isdigit()
                                    if not a:
                                        validar=False

                                else:
                                    if atributo.id_atributo.tipo == "LOG":
                                        if a != "Verdadero" and a != "Falso":
                                            validar=False

                            if validar==True:
                                aa=AtributoItem.objects.get(id=atributo.id)
                                aa.valor=a
                                aa.save()
                    return render_to_response('items/creacion_correcta.html',{'id_fase':fase.id}, context_instance=RequestContext(request))
            else:

                formulario = PrimeraFaseForm(instance=item_nuevo)
            return render_to_response('items/modificar_item_solicitud.html', { 'formulario': formulario,'fase':fase,'proyecto':proyecto, 'item':item_nuevo, 'atributos':atributos, 'atri':atri, 'archivos':archivos}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect ('/denegado')

    if flag==True and item_nuevo.estado=='BLO':
        return HttpResponse('<h1> No se puede modificar el item, ya que ya ha sido generada una solicitud de cambio para el mismo</h1>')

    if flag==True and item_nuevo.estado=='FIN':
        return render_to_response('solicitudes/peticion_modificar.html',{'id_item':item_nuevo.id,'fase':fase}, context_instance=RequestContext(request))
    if item_nuevo.estado=='PEN':

        if flag==True:

                if request.method=='POST':

                    formulario = PrimeraFaseForm(request.POST, instance=item_nuevo)

                    if formulario.is_valid():
                        generar_version(item_nuevo)
                        today = datetime.now() #fecha actual
                        dateFormat = today.strftime("%Y-%m-%d") # fecha con format

                        formulario.save()
                        item_nuevo.fecha_mod=dateFormat
                        item_nuevo.version=item_nuevo.version+1
                        item_nuevo.save()

                        return render_to_response('items/creacion_correcta.html',{'id_fase':fase.id}, context_instance=RequestContext(request))

                else:

                    formulario = PrimeraFaseForm(instance=item_nuevo)
                    hijo=True
                return render_to_response('items/editar_item.html', { 'formulario': formulario, 'item':item_nuevo, 'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))

        else:
                return render_to_response('403.html')
    else:
        return HttpResponse('<h1> No se puede modificar el item, ya que su estado no es Pendiente</h1>')






@login_required
def detalle_userStory(request):
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
    proyecto=Proyecto.objects.get(id=fasse.proyecto_id)
    if es_miembro(request.user.id, fase,''):
        atributos=AtributoItem.objects.filter(id_item=id_item)
        archivos=Archivo.objects.filter(id_item=id_item)
        dato = get_object_or_404(Item, pk=id_item)

        return render_to_response('items/detalle_item.html', {'datos': dato, 'atributos': atributos, 'archivos':archivos,'fase':fasse,'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')





@login_required
def eliminar_item(request, id_item):
    '''
    Vista que permite cambiar el estado del item a anulado, para ello se verifica que el mismo
    no tenga hijos y ademas que su estado sea pendiente
    '''
    item=get_object_or_404(Item, id=id_item)
    fase=item.tipo_item.fase_id
    if es_miembro(request.user.id,fase,'delete_item')!=True or item.estado=='ANU':
        return HttpResponseRedirect('/denegado')
    item=get_object_or_404(Item, id=id_item)
    if item.estado=='PEN':
        a=Item.objects.filter((Q(tipo='Hijo') & Q(relacion=item))).exclude(estado='ANU')
        if len(a)!=0:
            messages.add_message(request,settings.DELETE_MESSAGE,"No se puede eliminar un item que tenga hijos")
            titem=item.tipo_item
            items=Item.objects.filter(tipo_item_id=titem.id).exclude(estado='ANU')
            item=get_object_or_404(Item, id=id_item)
            id_fase=item.tipo_item.fase_id
            fase=get_object_or_404(Fase,id=id_fase)
            proyecto=Proyecto.objects.get(id=fase.proyecto_id)
            return render_to_response('items/listar_items.html', {'datos': items,'mensaje':0 ,'titem':titem,'fase':fase, 'nivel':3,'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            item.estado='ANU'
            item.save()
            titem=item.tipo_item
            items=Item.objects.filter(tipo_item_id=titem.id).exclude(estado='ANU')
            item=get_object_or_404(Item, id=id_item)
            id_fase=item.tipo_item.fase_id
            fase=get_object_or_404(Fase,id=id_fase)
            proyecto=Proyecto.objects.get(id=fase.proyecto_id)
            return render_to_response('items/listar_items.html', {'datos': items,'mensaje':1 ,'titem':titem,'fase':fase, 'nivel':3,'proyecto':proyecto}, context_instance=RequestContext(request))
            messages.add_message(request,settings.DELETE_MESSAGE,"Item eliminado correctamente")
    else:
         messages.add_message(request,settings.DELETE_MESSAGE,"No se puede eliminar un item cuyo estado no sea pendiente")
         titem=item.tipo_item
         items=Item.objects.filter(tipo_item_id=titem.id).exclude(estado='ANU')
         item=get_object_or_404(Item, id=id_item)
         id_fase=item.tipo_item.fase_id
         fase=get_object_or_404(Fase,id=id_fase)
         proyecto=Proyecto.objects.get(id=fase.proyecto_id)
         return render_to_response('items/listar_items.html', {'datos': items,'mensaje':2 ,'titem':titem,'fase':fase, 'nivel':3,'proyecto':proyecto}, context_instance=RequestContext(request))
    id_fase=item.tipo_item.fase_id
    titem=item.tipo_item
    id_proyecto=Fase.objects.get(id=fase).proyecto_id
    nivel=3
    request.session['nivel'] = 3
    items=Item.objects.filter(tipo_item_id=titem.id).exclude(estado='ANU')
    proyecto=Proyecto.objects.get(id=id_proyecto)
    fase=Fase.objects.filter(id=id_fase)
    return render_to_response('items/listar_items.html', {'datos': items,'mensaje':1000 ,'titem':titem,'fase':fase, 'nivel':nivel,'proyecto':proyecto}, context_instance=RequestContext(request))






