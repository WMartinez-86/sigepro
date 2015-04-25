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
from apps.userStories.forms import EstadoUSForm, PrimerFlujoForm
from django import forms


def userStoriesProyecto(proyecto):
    '''
    Funcion que recibe como parametro un proyecto y retorna todos los userStories del mismo
    '''
    flujos = Flujo.objects.filter(proyecto_id=proyecto)
    userStories=[]
    for flujo in flujos:
             if i.estado!='ANU':
                userStories.append(i)
    return userStories


@login_required
def crear_userStory(request,id_tipoUserStory):
    """
    Vista para crear un userStory. Ademas se dan las opciones de agregar un
    archivo al userStory, y de completar todos los atributos de su tipo de userStory
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_tipoUserStory: clave foranea al tipoUserStory
    @ return render_to_response('userStories/...) o render_to_response('403.html')
    """
    # atri=1
    # id_flujo=TipoUserStory.objects.get(id=id_tipoUserStory).flujo_id
    # if len(atributos)==0:
    #     atri=0
    # flujo=Flujo.objects.get(id=id_flujo)
    # proyecto=flujo.proyecto_id
    # userStories=[]
    # tipouserStory=[]
    # flujo_anterior=Flujo.objects.filter(proyecto_id=proyecto, orden=((flujo.orden)-1))
    # if len(flujo_anterior)==0:
    #     userStories=[]
    # else:
    #     for flujo in flujo_anterior:
    #         tuserStory=TipoUserStory.objects.filter(flujo_id=flujo.id)
    #          for i in tuserStory:
    #             it=UserStory.objects.filter(tipo_userStory_id=i.id, estado='FIN')
    #             for ii in it:
    #                 userStories.append(ii)
    #
    # if flag==True:
    #     if request.method=='POST':
    #         #formset = UserStoryFormSet(request.POST)
    #         formulario = PrimerFlujoForm(request.POST)
    #
    #         if formulario.is_valid():
    #             today = datetime.now() #fecha actual
    #             dateFormat = today.strftime("%Y-%m-%d") # fecha con format
    #             #obtener userStory con el cual relacionar
    #             userStory_nombre=request.POST.get('entradalista')
    #             if userStory_nombre!=None:
    #                 userStory=''
    #                 userStoriess=UserStory.objects.filter(nombre=userStory_nombre)
    #                 for i in userStoriess:
    #                     userStory=i
    #                 cod=newUserStory=UserStory(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1, relacion_id=userStory.id, tipo='Sucesor',tipo_userStory_id=id_tipoUserStory,fecha_creacion=dateFormat, fecha_mod=dateFormat,flujo_id=id_flujo)
    #                 newUserStory.save()
    #             else:
    #                 cod=newUserStory=UserStory(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1,tipo_userStory_id=id_tipoUserStory,fecha_creacion=dateFormat, fecha_mod=dateFormat,flujo_id=id_flujo)
    #                 newUserStory.save()
    #         #guardar archivo
    #             if request.FILES.get('file')!=None:
    #                 archivo=Archivo(archivo=request.FILES['file'],nombre='', id_userStory_id=cod.id)
    #                 archivo.save()
    #         #guardar atributos
    #
    #             for atributo in atributos:
    #                  a=request.POST.get(atributo.nombre)
    #                 if a!=None:
    #                     #validar atributos antes de guardarlos
    #                     #if validarAtributo(request,atributo.tipo,a):
    #                         aa=AtributoUserStory(id_userStory_id=cod.id, id_atributo=atributo,valor=a,version=1)
    #                         aa.save()
    #             return render_to_response('userStories/creacion_correcta.html',{'id_flujo':id_flujo}, context_instance=RequestContext(request))
    #     else:
    #
    #         formulario = PrimerFlujoForm()
    #         hijo=False
    #         proyecto=Proyecto.objects.filter(id=flujo.proyecto_id)
    #         return render_to_response('userStories/crear_userStory.html', { 'formulario': formulario, 'atributos':atributos, 'userStories':userStories, 'hijo':hijo,'atri':atri,'tuserStory':id_tipoUserStory,'flujo':flujo}, context_instance=RequestContext(request))
    # else:
    #     return render_to_response('403.html')


def puede_add_userStories(id_flujo):
    """
    Funcion que verifica que ya se pueden agregar userStories a una flujo. Si es la primera flujo, se puede
    Si no, se verifica que la flujo anterior tenga userStories en una linea base para poder agregar userStories a la
    flujo siguiente.
    @param id_flujo: clave foranea a la flujo
    @return: boolean
    """
    flujo=Flujo.objects.get(id=id_flujo)
    if flujo.orden==1:
        return True
    else:
        flujo_anterior=Flujo.objects.get(orden=flujo.orden-1,proyecto=flujo.proyecto)
        tipouserStory=TipoUserStory.objects.filter(flujo_id=flujo_anterior.id)

        for ti in tipouserStory:
            userStory=UserStory.objects.filter(tipo_userStory_id=ti.id)
            for i in userStory:
                if i.estado=='FIN':
                    return True
    return False

@login_required
def listar_userStories(request,id_flujo):
    """
    vista para listar los userStories pertenecientes a la flujo
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_userStory: clave foranea a la flujo
    @return render_to_response(..) o HttpResponse(...)
    """
    tuserStory=get_object_or_404(Flujo,id=id_flujo)
    flujo=Flujo.objects.filter(id=id_flujo)
    if es_miembro(request.user.id,flujo,''):
        userStories=UserStory.objects.filter(flujo_id=id_flujo).exclude(estado='ANU')
        if puede_add_userStories(flujo):
            nivel = 3
            id_proyecto=Flujo.objects.get(id=flujo).proyecto_id
            proyecto=Proyecto.objects.get(id=id_proyecto)
            return render_to_response('userStories/listar_userStories.html', {'datos': userStories, 'flujo':tuserStory, 'nivel':nivel,'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            #ESTE HAY QUE CORREGIR SI HAY TIEMPO
            return HttpResponse("<h1>No se pueden administrar los UserStories de esta flujo. La flujo anterior aun no tiene userStories finalizados<h1>")

    else:
        return render_to_response('403.html')


def editar_userStory(request,id_userStory):
    '''
    vista para cambiar el nombre y la descripcion del tipo de userStory, y ademas agregar atributos al mismo
    Si el userStory se encuentra con el estado CON (solicitud de cambio aprobada), se puede modificar el userStory solo si el
    usuario es el que realizo la solicittud de cambio
    '''

    userStory_nuevo=get_object_or_404(UserStory,id=id_userStory)
    flujo=Flujo.objects.get(id=userStory_nuevo.flujo_id)
    proyecto=Proyecto.objects.get(id=flujo.proyecto_id)
    flag=es_miembro(request.user.id,userStory_nuevo.flujo_id,'change_userStory')
    atri=1
    if flag==False:
        return HttpResponseRedirect('/denegado')

    atributos=AtributoUserStory.objects.filter(id_userStory=id_userStory)
    if len(atributos)==0:
        atri=0
    if userStory_nuevo.estado=='CON':
        archivos=Archivo.objects.filter(id_userStory=userStory_nuevo)
        solicitudes=Solicitud.objects.filter(userStory=userStory_nuevo, estado='APROBADA')
        solicitud=solicitudes[0]
        solicitante=solicitud.usuario
        if request.user==solicitante:
            if request.method=='POST':
                formulario = PrimerFlujoForm(request.POST, instance=userStory_nuevo)

                if formulario.is_valid():

                    if request.FILES.get('file')!=None:
                        archivo=Archivo(archivo=request.FILES['file'],nombre='', id_userStory_id=id_userStory)
                        archivo.save()
                    #generar_version(userStory_nuevo,request.user)
                    today = datetime.now() #fecha actual
                    dateFormat = today.strftime("%Y-%m-%d") # fecha con format

                    formulario.save()
                    userStory_nuevo.fecha_mod=dateFormat
                    #userStory_nuevo.version=userStory_nuevo.version+1
                    userStory_nuevo.save()

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
                                aa=AtributoUserStory.objects.get(id=atributo.id)
                                aa.valor=a
                                aa.save()
                    return render_to_response('userStories/creacion_correcta.html',{'id_flujo':flujo.id}, context_instance=RequestContext(request))
            else:

                formulario = PrimerFlujoForm(instance=userStory_nuevo)
            return render_to_response('userStories/modificar_userStory_solicitud.html', { 'formulario': formulario,'flujo':flujo,'proyecto':proyecto, 'userStory':userStory_nuevo, 'atributos':atributos, 'atri':atri, 'archivos':archivos}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect ('/denegado')

    if flag==True and userStory_nuevo.estado=='BLO':
        return HttpResponse('<h1> No se puede modificar el userStory, ya que ya ha sido generada una solicitud de cambio para el mismo</h1>')

    if flag==True and userStory_nuevo.estado=='FIN':
        return render_to_response('solicitudes/peticion_modificar.html',{'id_userStory':userStory_nuevo.id,'flujo':flujo}, context_instance=RequestContext(request))
    if userStory_nuevo.estado=='PEN':

        if flag==True:

                if request.method=='POST':

                    formulario = PrimerFlujoForm(request.POST, instance=userStory_nuevo)

                    if formulario.is_valid():
                        generar_version(userStory_nuevo)
                        today = datetime.now() #fecha actual
                        dateFormat = today.strftime("%Y-%m-%d") # fecha con format

                        formulario.save()
                        userStory_nuevo.fecha_mod=dateFormat
                        userStory_nuevo.version=userStory_nuevo.version+1
                        userStory_nuevo.save()

                        return render_to_response('userStories/creacion_correcta.html',{'id_flujo':flujo.id}, context_instance=RequestContext(request))

                else:

                    formulario = PrimerFlujoForm(instance=userStory_nuevo)
                    hijo=True
                return render_to_response('userStories/editar_userStory.html', { 'formulario': formulario, 'userStory':userStory_nuevo, 'flujo':flujo,'proyecto':proyecto}, context_instance=RequestContext(request))

        else:
                return render_to_response('403.html')
    else:
        return HttpResponse('<h1> No se puede modificar el userStory, ya que su estado no es Pendiente</h1>')

@login_required
def listar_archivos(request, id_userStory):
    """
    vista para gestionar los archivos de un userStory dado
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_userStory: clave foranea al userStory
    @return render_to_response(..)
    """

    tuserStory=get_object_or_404(UserStory,id=id_userStory).tipo_userStory
    flujo=tuserStory.flujo_id
    if es_miembro(request.user.id,flujo,'change_userStory'):
        if request.method=='POST':
            if request.FILES.get('file')!=None:
                archivo=Archivo(archivo=request.FILES['file'],nombre='', id_userStory_id=id_userStory)
                archivo.save()
        archivos=Archivo.objects.filter(id_userStory=id_userStory)
        flujo=Flujo.objects.get(id=tuserStory.flujo_id)
        proyecto=Proyecto.objects.get(id=flujo.proyecto_id)
        return render_to_response('userStories/listar_archivos.html', { 'archivos': archivos,'tuserStory':id_userStory,'flujo':flujo,'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')

@login_required

def eliminar_archivo(request, id_archivo):
    """
    vista que recibe el id de un archivo y lo borra de la base de datos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_archivo: clave foranea al archivo a eliminar
    @return HttpResponseRedirect('/desarrollo/userStory/archivos/'+str(userStory.id))
    """

    archivo=get_object_or_404(Archivo,id=id_archivo)
    userStory=archivo.id_userStory
    if userStory.estado!='PEN' and userStory.estado!='CON':
        return HttpResponse("<h1> No se puede modificar un userStory cuyo estado no sea pendiente")
    tuserStory=userStory.tipo_userStory
    flujo=tuserStory.flujo
    if es_miembro(request.user.id, flujo.id, 'delete_archivo')!=True:
        return HttpResponseRedirect('/denegado')
    archivo.delete()
    if userStory.estado=='PEN':
        return HttpResponseRedirect('/desarrollo/userStory/archivos/'+str(userStory.id))
    if userStory.estado=='CON':
        return HttpResponseRedirect('/desarrollo/userStory/modificar/'+str(userStory.id))

@login_required
def detalle_userStory(request, id_userStory):
    """
    vista para ver los detalles del userStory <id_userStory>
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_userStory: clave foranea al userStory
    @return render_to_response(..)
    """
    userStory=get_object_or_404(UserStory,id=id_userStory)
    tipouserStory=get_object_or_404(TipoUserStory,id=userStory.tipo_userStory_id)
    flujo=tipouserStory.flujo_id
    fasse=Flujo.objects.get(id=flujo)
    proyecto=Proyecto.objects.get(id=fasse.proyecto_id)
    if es_miembro(request.user.id, flujo,''):
        atributos=AtributoUserStory.objects.filter(id_userStory=id_userStory)
        archivos=Archivo.objects.filter(id_userStory=id_userStory)
        dato = get_object_or_404(UserStory, pk=id_userStory)

        return render_to_response('userStories/detalle_userStory.html', {'datos': dato, 'atributos': atributos, 'archivos':archivos,'flujo':fasse,'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')


def descargar(idarchivo):
    """
    Funcion que recibe el id de un archivo y retorna el objeto archivo dado el id recibido
    @param idarchivo: clave al archivo
    @return archivo.archivo
    """
    archivo=get_object_or_404(Archivo,id=idarchivo)

    return archivo.archivo

@login_required
def descargo_archivo(request, idarchivo):
    """
    Vista para descargar un archivo de un userStory especifico
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_userStory: clave foranea al archivo a cargar
    @return StreamingHttpResponse(descargar(idarchivo),content_type='application/force-download')
    """
    return StreamingHttpResponse(descargar(idarchivo),content_type='application/force-download')


@login_required
def cambiar_estado_userStory(request,id_userStory):
    """
    vista para cambiar el estado de un userStory, teniendo en cuenta:
    1) Si se quiere pasar de PEN  a VAL, se verifica que el estado de su padre tambien sea VAL
    2) Si se quiere pasar de VAL a PEN se verifica que el estado de sus hijos tambien sea PEN
    3) Si quiere pasar un userStory de REV a VAL, el userStory que origino la solicitud de cambio debe estar con estado FIN y
        solo el lider puede cambiar este estado
    4) Si se quiere cambiar el estado de un userStory CON a VAL, se verifica que solo el que tiene la credencial pueda
    cambiar el estado, y al cambiarlo, se crea una nueva linea base con todos los userStories de la anterior, se cambia el
    estado del userStory a FIN y el estado de la solicitud a EJECUTADA
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_userStory: clave foranea al userStory
    @return render_to_response('userStories/...) de acuerdo a los diferentes estados que puede tener un userStory
    """

    userStory=get_object_or_404(UserStory,id=id_userStory)

    nombre=userStory.nombre
    flujo=userStory.tipo_userStory.flujo
    lider=flujo.proyecto.lider
    proyecto=Proyecto.objects.get(id=flujo.proyecto_id)
    if not es_miembro(request.user.id, flujo.id,''):
        return HttpResponseRedirect ('/denegado')
    tuserStory=userStory.tipo_userStory_id

    if userStory.estado=='REV' or userStory.estado=='CON':
        estado_anterior=userStory.estado
        if lider!=request.user and userStory.estado=='REV':
            return HttpResponseRedirect ('/denegado')
        solicitudes=Solicitud.objects.filter(userStory=userStory, estado='APROBADA')
        if solicitudes is None and userStory.estado=='CON':
            return HttpResponseRedirect ('/denegado')
        if len(solicitudes)==0:
            solicitud=None
            solicitante=None
        else:
            solicitud=solicitudes[0]
            solicitante=solicitud.usuario
        if (solicitante!=request.user and userStory.estado=='CON'):
            print(solicitante)
            return HttpResponseRedirect ('/denegado')
        if request.method == 'POST':
            userStory_form = EstadoUSForm(request.POST, instance=userStory)
            if userStory_form.is_valid():
                    puede_modificar=True
                    if userStory_form.cleaned_data['estado']=='VAL':
                        if estado_anterior=='CON':
                            #se obtienen todos los userStories perteneciente a la linea base rota
                            userStory=get_object_or_404(UserStory, id=id_userStory)
                            userStoriesLineaBase=UserStory.objects.filter(lineaBase=userStory.lineaBase)
                            #se crea una linea base nueva
                            vieja_lb=userStory.lineaBase
                            cod=nueva_lb=LineaBase(nombre=vieja_lb.nombre+ ' Nueva', flujo=vieja_lb.flujo, estado='CERRADA')
                            nueva_lb.save()
                            for userStoryLB in userStoriesLineaBase:
                                #se genera una nueva version para cada userStory
                                generar_version(userStoryLB)
                                #se agrega cada userStory a la nueva linea base
                                instanciaUserStory=get_object_or_404(UserStory, id=userStoryLB.id)
                                instanciaUserStory.version=userStory.version+1
                                instanciaUserStory.lineaBase=cod
                                instanciaUserStory.save()
                            #se cambia el estado del userStory a FIN
                            userStory.estado='FIN'
                            userStory.version=userStory.version+1
                            userStory.lineaBase=cod
                            userStory.save()
                            #se cambia el estado de la solicitud de cambio a ejecutada
                            solicitud.estado='EJECUTADA'
                            solicitud.save()
                            #se borran de la lista los userStories que estan relacionados con el userStory modificado
                            userStories_revision=UserStoriesARevision.objects.filter(userStory_bloqueado=userStory)
                            for userStoryRev in userStories_revision:
                                instanciaUserStoryRev=get_object_or_404(UserStoriesARevision, id=userStoryRev.id)
                                instanciaUserStoryRev.delete()
                            return render_to_response('userStories/creacion_correcta.html',{'id_flujo':flujo.id}, context_instance=RequestContext(request))
                        else:
                            userStories_revision=UserStoriesARevision.objects.all()

                            for userStoryR in userStories_revision:
                                if userStoryR.userStory_revision.id==userStory.id:
                                    puede_modificar=False
                                    break

                            if puede_modificar==False:
                                messages.add_message(request,settings.DELETE_MESSAGE, 'No se puede validar el userStory porque aun no se han aplicado los cambios de la solicitud')
                                return render_to_response('userStories/cambiar_estado_userStory.html', { 'userStory_form': userStory_form, 'nombre':nombre, 'tuserStory':userStory,'mensaje':3,'flujo':flujo,'proyecto':proyecto}, context_instance=RequestContext(request))
                            else:
                                if userStory.lineaBase is None:
                                    userStory.estado='VAL'
                                else:
                                    userStory.estado='FIN'
                                userStory.save()
                                return render_to_response('userStories/creacion_correcta.html',{'id_flujo':flujo.id}, context_instance=RequestContext(request))
                    else:
                        messages.add_message(request,settings.DELETE_MESSAGE, 'El estado no puede cambiar de en Revision/Construccion A Pendiente')
                        id_flujo=get_object_or_404(UserStory,id=id_userStory).flujo_id
                        flujo=Flujo.objects.get(id=id_flujo)
                        return render_to_response('userStories/cambiar_estado_userStory.html', {  'userStory_form': userStory_form, 'nombre':nombre, 'tuserStory':userStory,'mensaje':2,'flujo':flujo,'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            # formulario inicial
            userStory_form = EstadoUSForm(instance=userStory)
            id_flujo=get_object_or_404(UserStory,id=id_userStory).flujo_id
            flujo=Flujo.objects.get(id=id_flujo)
        return render_to_response('userStories/cambiar_estado_userStory.html', {  'userStory_form': userStory_form, 'nombre':nombre, 'tuserStory':userStory,'mensaje':100,'flujo':flujo,'proyecto':proyecto}, context_instance=RequestContext(request))


    id_flujo=get_object_or_404(UserStory,id=id_userStory).flujo_id
    flujo=Flujo.objects.get(id=id_flujo)

    nombre=userStory.nombre
    tuserStory=userStory.tipo_userStory_id
    if userStory.estado=='FIN':
        return HttpResponse('<h1>No se puede cambiar el estado de un userStory finalizado<h1>')
    if request.method == 'POST':
        bandera=False
        userStory_form = EstadoUSForm(request.POST, instance=userStory)
        if userStory_form.is_valid():
                    if userStory_form.cleaned_data['estado']=='VAL':
                        if userStory.tipo=='Hijo':
                            papa=userStory.relacion
                            if papa.estado=='PEN' or papa.estado=='REV' or papa.estado=='BLO' or papa.estado=='CON':
                                messages.add_message(request,settings.DELETE_MESSAGE,'No se puede cambiar a Validado ya que su padre no ha sido validado o Finalizado')
                                #'No se puede cambiar a Validado ya que su padre no ha sido validado o Finalizado'
                                return render_to_response('userStories/cambiar_estado_userStory.html', { 'userStory_form': userStory_form, 'nombre':nombre, 'tuserStory':userStory,'mensaje':0,'flujo':flujo,'proyecto':proyecto}, context_instance=RequestContext(request))
                                bandera=True
                            if papa.estado=='VAL' or papa.estado=='FIN':
                                bandera=False
                    if userStory_form.cleaned_data['estado']=='PEN':
                            hijos=UserStory.objects.filter(relacion=userStory).exclude(estado='ANU')
                            for hijo in hijos:
                                if hijo.estado!='PEN' and hijo.tipo=='Hijo':
                                    # 'No se puede cambiar  a pendiente ya que tiene hijos con estados distintos a Pendiente'
                                    return render_to_response('userStories/cambiar_estado_userStory.html', { 'userStory_form': userStory_form, 'nombre':nombre, 'tuserStory':userStory,'mensaje':1,'flujo':flujo,'proyecto':proyecto}, context_instance=RequestContext(request))
                                    bandera=True
                    if bandera==True:
                        return render_to_response('userStories/cambiar_estado_userStory.html', { 'userStory_form': userStory_form, 'nombre':nombre, 'tuserStory':userStory,'mensaje':100,'flujo':flujo,'proyecto':proyecto}, context_instance=RequestContext(request))
                    else:
                        userStory_form.save()
                        return render_to_response('userStories/creacion_correcta.html',{'id_flujo':id_flujo}, context_instance=RequestContext(request))

    else:
        # formulario inicial
        userStory_form = EstadoUSForm(instance=userStory)
        return render_to_response('userStories/cambiar_estado_userStory.html', { 'userStory_form': userStory_form, 'nombre':nombre,'tuserStory':userStory,'mensaje':100,'flujo':flujo,'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required
def eliminar_userStory(request, id_userStory):
    '''
    Vista que permite cambiar el estado del userStory a anulado, para ello se verifica que el mismo
    no tenga hijos y ademas que su estado sea pendiente
    '''
    userStory=get_object_or_404(UserStory, id=id_userStory)
    flujo=userStory.tipo_userStory.flujo_id
    if es_miembro(request.user.id,flujo,'delete_userStory')!=True or userStory.estado=='ANU':
        return HttpResponseRedirect('/denegado')
    userStory=get_object_or_404(UserStory, id=id_userStory)
    if userStory.estado=='PEN':
        a=UserStory.objects.filter((Q(tipo='Hijo') & Q(relacion=userStory))).exclude(estado='ANU')
        if len(a)!=0:
            messages.add_message(request,settings.DELETE_MESSAGE,"No se puede eliminar un userStory que tenga hijos")
            tuserStory=userStory.tipo_userStory
            userStories=UserStory.objects.filter(tipo_userStory_id=tuserStory.id).exclude(estado='ANU')
            userStory=get_object_or_404(UserStory, id=id_userStory)
            id_flujo=userStory.tipo_userStory.flujo_id
            flujo=get_object_or_404(Flujo,id=id_flujo)
            proyecto=Proyecto.objects.get(id=flujo.proyecto_id)
            return render_to_response('userStories/listar_userStories.html', {'datos': userStories,'mensaje':0 ,'tuserStory':tuserStory,'flujo':flujo, 'nivel':3,'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            userStory.estado='ANU'
            userStory.save()
            tuserStory=userStory.tipo_userStory
            userStories=UserStory.objects.filter(tipo_userStory_id=tuserStory.id).exclude(estado='ANU')
            userStory=get_object_or_404(UserStory, id=id_userStory)
            id_flujo=userStory.tipo_userStory.flujo_id
            flujo=get_object_or_404(Flujo,id=id_flujo)
            proyecto=Proyecto.objects.get(id=flujo.proyecto_id)
            return render_to_response('userStories/listar_userStories.html', {'datos': userStories,'mensaje':1 ,'tuserStory':tuserStory,'flujo':flujo, 'nivel':3,'proyecto':proyecto}, context_instance=RequestContext(request))
            messages.add_message(request,settings.DELETE_MESSAGE,"UserStory eliminado correctamente")
    else:
         messages.add_message(request,settings.DELETE_MESSAGE,"No se puede eliminar un userStory cuyo estado no sea pendiente")
         tuserStory=userStory.tipo_userStory
         userStories=UserStory.objects.filter(tipo_userStory_id=tuserStory.id).exclude(estado='ANU')
         userStory=get_object_or_404(UserStory, id=id_userStory)
         id_flujo=userStory.tipo_userStory.flujo_id
         flujo=get_object_or_404(Flujo,id=id_flujo)
         proyecto=Proyecto.objects.get(id=flujo.proyecto_id)
         return render_to_response('userStories/listar_userStories.html', {'datos': userStories,'mensaje':2 ,'tuserStory':tuserStory,'flujo':flujo, 'nivel':3,'proyecto':proyecto}, context_instance=RequestContext(request))
    id_flujo=userStory.tipo_userStory.flujo_id
    tuserStory=userStory.tipo_userStory
    id_proyecto=Flujo.objects.get(id=flujo).proyecto_id
    nivel=3
    request.session['nivel'] = 3
    userStories=UserStory.objects.filter(tipo_userStory_id=tuserStory.id).exclude(estado='ANU')
    proyecto=Proyecto.objects.get(id=id_proyecto)
    flujo=Flujo.objects.filter(id=id_flujo)
    return render_to_response('userStories/listar_userStories.html', {'datos': userStories,'mensaje':1000 ,'tuserStory':tuserStory,'flujo':flujo, 'nivel':nivel,'proyecto':proyecto}, context_instance=RequestContext(request))
