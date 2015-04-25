from django.shortcuts import render
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
from apps.userStories.models import UserStories
from apps.proyectos.models import Proyecto
# from apps.lineaBase.models import LineaBase
# from apps.tiposDeItem.models import TipoItem, Atributo
# from apps.items.forms import EstadoItemForm, PrimeraFaseForm, SolicitudCambioForm
# from apps.solicitudes.models import Solicitud,Voto, ItemsARevision
from django import forms


# Create your views here.

@login_required

def crear_userStories(request,id_tipoItem):
    """
    Vista para crear un item y asignarlo a un tipo de item. Ademas se dan las opciones de agregar un
    archivo al item, y de completar todos los atributos de su tipo de item
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_tipoItem: clave foranea al tipoItem
    @ return render_to_response('items/...) o render_to_response('403.html')
    """
    atri=1
    if cantidad_items(id_tipoItem):
       # print(cantidad_items(id_tipoItem))
        id_fase=TipoItem.objects.get(id=id_tipoItem).fase_id
        flag=es_miembro(request.user.id,id_fase,'add_item')
        atributos=Atributo.objects.filter(tipoItem=id_tipoItem)
        if len(atributos)==0:
            atri=0
        fase=Fase.objects.get(id=id_fase)
        proyecto=fase.proyecto_id
        items=[]
        tipoitem=[]
        fase_anterior=Fase.objects.filter(proyecto_id=proyecto, orden=((fase.orden)-1))
        if len(fase_anterior)==0:
            items=[]
        else:
            for fase in fase_anterior:
                titem=TipoItem.objects.filter(fase_id=fase.id)
                for i in titem:
                    it=Item.objects.filter(tipo_item_id=i.id, estado='FIN')
                    for ii in it:
                        items.append(ii)

        if flag==True:
            if request.method=='POST':
                #formset = ItemFormSet(request.POST)
                formulario = PrimeraFaseForm(request.POST)

                if formulario.is_valid():
                    today = datetime.now() #fecha actual
                    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
                    #obtener item con el cual relacionar
                    item_nombre=request.POST.get('entradalista')
                    if item_nombre!=None:
                        item=''
                        itemss=Item.objects.filter(nombre=item_nombre)
                        for i in itemss:
                            item=i
                        cod=newItem=Item(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1, relacion_id=item.id, tipo='Sucesor',tipo_item_id=id_tipoItem,fecha_creacion=dateFormat, fecha_mod=dateFormat,fase_id=id_fase)
                        newItem.save()
                    else:
                        cod=newItem=Item(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1,tipo_item_id=id_tipoItem,fecha_creacion=dateFormat, fecha_mod=dateFormat,fase_id=id_fase)
                        newItem.save()
                #guardar archivo
                    if request.FILES.get('file')!=None:
                        archivo=Archivo(archivo=request.FILES['file'],nombre='', id_item_id=cod.id)
                        archivo.save()
                #guardar atributos

                    for atributo in atributos:

                        a=request.POST.get(atributo.nombre)
                        if a!=None:
                            #validar atributos antes de guardarlos
                            #if validarAtributo(request,atributo.tipo,a):
                                aa=AtributoItem(id_item_id=cod.id, id_atributo=atributo,valor=a,version=1)
                                aa.save()
                    return render_to_response('items/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))
            else:

                formulario = PrimeraFaseForm()
                hijo=False
                proyecto=Proyecto.objects.filter(id=fase.proyecto_id)
                return render_to_response('items/crear_item.html', { 'formulario': formulario, 'atributos':atributos, 'items':items, 'hijo':hijo,'atri':atri,'titem':id_tipoItem,'fase':fase}, context_instance=RequestContext(request))
        else:
            return render_to_response('403.html')
    else:
        id_fase=get_object_or_404(TipoItem,id=id_tipoItem).fase_id
        return render_to_response('items/cantidad_maxima.html',{'id_fase':id_fase}, context_instance=RequestContext(request))




@login_required

def listar_userStories(request,id_flujo):
    """
    vista para listar los items pertenecientes a la fase
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea a la fase
    @return render_to_response(..) o HttpResponse(...)
    """
    titem=get_object_or_404(Flujo,id=id_flujo)
    flujo=Flujo.objects.filter(id=id_flujo)
    if es_miembro(request.user.id,flujo,''):
        userStories=UserStories.objects.filter(fase_id=id_flujo).exclude(estado='ANU')

        nivel = 3
        id_proyecto=Flujo.objects.get(id=flujo).proyecto_id
        proyecto=Proyecto.objects.get(id=id_proyecto)
        render_to_response('userStories/listar_userStories.html', {'datos': userStories, 'fase':titem, 'nivel':nivel,'proyecto':proyecto}, context_instance=RequestContext(request))
        #else:
        #    #ESTE HAY QUE CORREGIR SI HAY TIEMPO
        #    return HttpResponse("<h1>No se pueden administrar los Items de esta fase. La fase anterior aun no tiene items finalizados<h1>")

    else:
        return render_to_response('403.html')



def es_miembro(id_usuario, id_flujo,permiso):
    """
    funcion que recibe el id de un usuario y de una fase y devuelve true si el usuario tiene alguna fase asignada
    o false si no tiene ningun rol en esa fase
    Ademas verifica que el estado de la fase se EJE
    @param id_usuario: clave foranea al usuario
    @param id_fase: clave foranea a la fase
    @return booelean
    """

    flujo=get_object_or_404(Flujo,id=id_flujo) #busca la fase
    usuario=User.objects.get(id=id_usuario) #busca el usuario
    proyecto=get_object_or_404(Proyecto,id=flujo.proyecto_id) #el proyecto
    if flujo.estado!='EJE':
        return False
    if usuario.id==proyecto.lider_id:
        return True
    rol_usuario=None
    roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
    roles_flujo=Group.objects.filter(flujo__id=flujo.id)
    for rol in roles:
        for r in roles_flujo:
            if rol.id==r.id:
                rol_usuario=rol
    if permiso=='' and rol_usuario!=None:
        return True
    if rol_usuario!=None:
        perm=Permission.objects.get(codename=permiso)
        permisos=Permission.objects.filter(group__id=rol_usuario.id)
        for p in permisos:
            if p==perm:
                return True

    return False


@login_required
def listar_proyectos(request):
    """
    vista para listar los proyectos asignados a un usuario expecifico
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('items/ingresar_proyecto.html', {'datos': setproyectos}, context_instance=RequestContext(request))
    """
    success_url = reverse_lazy('listar_proyectos')
    usuario = request.user
    request.session['cantSolicitudes']=contar_solicitudes(request.user.id)
    cantidad=contar_solicitudes(request.user.id)
    #proyectos del cual es lider y su estado es activo
    proyectosLider = Proyecto.objects.filter(lider_id=usuario.id, estado='ACT')

    roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
    fases=[]
    proyectos=[]
    #las fases de en las cuales el usuario tiene un rol

    for rol in roles:
        #print(rol.id)
        fase=Fase.objects.get(roles=rol.id)
        fases.append(fase)
    #los proyectos a los que pertenecen esas fases
    for fase in fases:
        proyecto=Proyecto.objects.get(id=fase.proyecto_id)
        if proyecto.estado=='ACT':
            proyectos.append(proyecto)
    for p in proyectosLider:
        proyectos.append(p)
    setproyectos=set(proyectos)
    return render_to_response('items/ingresar_proyecto.html', {'cantidadsolicitud':cantidad,'datos': setproyectos}, context_instance=RequestContext(request))



@login_required
def listar_flujos(request, id_proyecto):
    """
    vista para listar las fases asignadas a un usuario de un proyecto especifico
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: clave foranea al proyecto
    @return: render_to_response(...)
    """
    #busca todas las fases del proyecto
    fasesProyecto=Fase.objects.filter(proyecto_id=id_proyecto, estado='EJE').order_by('orden')
    usuario = request.user
    proyecto=get_object_or_404(Proyecto,id=id_proyecto)
    fases=[]
    #si es lider pertenece a todas las fases
    if usuario.id==proyecto.lider_id:
        fases=fasesProyecto
    #si no, busca todas las fases en las que tiene algun rol asignado
    else:
        roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
        for rol in roles:
            for f in fasesProyecto:
                ff=Fase.objects.filter(id=f.id,roles__id=rol.id)
                for fff in ff:
                    fases.append(fff)
    #si no encuentra ninguna fase, significa que alguien que no tiene permisos esta tratando de ver
    #fases que no le correponden, se redirige al template de prohibido
    if len(fases)==0:
        return render_to_response('403.html')
    nivel = 1
    return render_to_response('items/ingresar_fase.html', {'datos': fases, 'nivel':nivel, 'proyecto':proyecto}, context_instance=RequestContext(request))