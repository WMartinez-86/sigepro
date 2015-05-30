# -*- encoding: utf-8 -*-

__text__ = 'Este modulo contiene funciones que permiten el control de las flujos'

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.flujos.models import Flujo
from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
from django.contrib import messages
from sigepro import settings
from django.contrib import messages
from django.shortcuts import render
from apps.proyectos.models import Proyecto
from apps.flujos.forms import FlujoForm, ModificarFlujoForm, CrearFlujoForm
from apps.roles.forms import GroupForm
from datetime import datetime
from apps.userStories.models import UserStory
from apps.actividades.models import Actividad


@login_required
@permission_required('flujo')
def registrar_flujo(request, id_proyecto):
    """
    Vista para registrar un nuevo flujo dentro de proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return HttpResponseRedirect('/flujos/register/success') si el rol fue correctamente asignado o
    render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request)) al formulario
    """
    mensaje=100
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if request.method=='POST':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        formulario = CrearFlujoForm(request.POST)
        if formulario.is_valid():
            newFlujo = Flujo(nombre = request.POST["nombre"],descripcion = request.POST["descripcion"],
                               estado = "PRO", proyecto_id = id_proyecto)
            orden=Flujo.objects.filter(proyecto_id=id_proyecto)
            proyecto=Proyecto.objects.get(id=id_proyecto)
            cantidad = orden.count()
            if cantidad>0:
                newFlujo.orden=orden.count()+1 # Calculo del orden del flujo a crear
                newFlujo.save()
                return render_to_response('flujos/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
            else:
                newFlujo.orden=1
                newFlujo.save()
                return render_to_response('flujos/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = CrearFlujoForm() #formulario inicial
    return render_to_response('flujos/registrar_flujos.html',{'formulario':formulario,'id':id_proyecto, 'proyecto':proyecto, 'mensaje':mensaje},
                              context_instance=RequestContext(request))



@login_required
@permission_required('proyectos, flujos')
def listar_flujos(request,id_proyecto):
    """
    vista para listar los flujos del proyectos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('flujos/listar_flujos.html', {'datos': flujos}, context_instance=RequestContext(request))
    """
    mensaje = 0 # sin errores
    flujos = Flujo.objects.filter(proyecto_id=id_proyecto).order_by('orden')
    proyecto = Proyecto.objects.get(id=id_proyecto)
    return render_to_response('flujos/listar_flujos.html', {'datos': flujos, 'proyecto' : proyecto, 'mensaje': mensaje}, context_instance=RequestContext(request))


@login_required
@permission_required('proyectos, flujos')
def editar_flujo(request,id_flujo):
    """
    Vista para editar un proyecto,y flujo
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: HttpResponseRedirect('/proyectos/register/success/') cuando el formulario es validado correctamente o render_to_response('proyectos/editar_proyecto.html', { 'proyectos': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))
    """
    flujo= Flujo.objects.get(id=id_flujo)
    id_proyecto= flujo.proyecto_id
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if proyecto.estado!='PRO':
        proyectos = Proyecto.objects.all().exclude(estado='ELI')
        return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos,'mensaje':1},
                              context_instance=RequestContext(request))
    if request.method == 'POST':
        # formulario enviado
        mensaje =100
        flujo_form = ModificarFlujoForm(request.POST, instance=flujo)
        if flujo_form.is_valid():
            if len(str(request.POST["fInicio"])) != 10 : #comprobacion de formato de fecha
                mensaje=0
                return render_to_response('flujos/editar_flujo.html', { 'form': flujo_form,'mensaje':mensaje, 'flujo': flujo, 'proyecto':proyecto},
                                          context_instance=RequestContext(request))
            else:
                fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%Y')
                fecha=fecha.strftime('%Y-%m-%d')
                fecha1=datetime.strptime(fecha,'%Y-%m-%d')
                proyecto=Proyecto.objects.get(id=flujo.proyecto_id)
                orden=Flujo.objects.filter(proyecto_id=proyecto.id)
                cantidad = orden.count()
                if cantidad>1 and flujo.orden != cantidad and flujo.orden >1: #comprobaciones de fechas
                       anterior = Flujo.objects.get(orden=(flujo.orden)-1, proyecto_id=id_proyecto)
                       siguiente = Flujo.objects.get(orden=(flujo.orden)+1, proyecto_id=id_proyecto)
                       if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                            mensaje=1
                            return render_to_response('flujos/editar_flujo.html', { 'form': flujo_form,'mensaje':mensaje, 'flujo': flujo, 'proyecto':proyecto},
                                                      context_instance=RequestContext(request))
                       else:
                           if fecha1>datetime.strptime(str(siguiente.fInicio),'%Y-%m-%d'):
                               mensaje=2
                               return render_to_response('flujos/editar_flujo.html', { 'form': flujo_form,'mensaje':mensaje, 'flujo': flujo, 'proyecto':proyecto},
                                                         context_instance=RequestContext(request))
                           else:
                                if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                                    mensaje=3
                                    return render_to_response('flujos/editar_flujo.html', { 'form': flujo_form,'mensaje':mensaje, 'flujo': flujo, 'proyecto':proyecto},
                                                              context_instance=RequestContext(request))
                                else:
                                    flujo_form.save()
                                    return render_to_response('flujos/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                elif cantidad>1 and flujo.orden != cantidad and flujo.orden==1:
                   siguiente = Flujo.objects.get(orden=(flujo.orden)+1, proyecto_id=id_proyecto)
                   if fecha1>datetime.strptime(str(siguiente.fInicio),'%Y-%m-%d'):
                        mensaje=2
                        return render_to_response('flujos/editar_flujo.html', { 'form': flujo_form,'mensaje':mensaje, 'flujo': flujo, 'proyecto':proyecto},
                                                  context_instance=RequestContext(request))
                   else:
                        if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                            mensaje=3
                            return render_to_response('flujos/editar_flujo.html', { 'form': flujo_form,'mensaje':mensaje, 'flujo': flujo, 'proyecto':proyecto},
                                                      context_instance=RequestContext(request))
                        else:
                            flujo_form.save()

                            return render_to_response('flujos/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                elif cantidad>1 and flujo.orden == cantidad:
                    anterior = Flujo.objects.get(orden=(flujo.orden)-1, proyecto_id=id_proyecto)
                    if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                        mensaje=1
                        return render_to_response('flujos/editar_flujo.html', { 'form': flujo_form,'mensaje':mensaje, 'flujo': flujo, 'proyecto':proyecto},
                                                  context_instance=RequestContext(request))
                    else:
                        if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                            mensaje=3
                            return render_to_response('flujos/editar_flujo.html', { 'form': flujo_form,'mensaje':mensaje, 'flujo': flujo, 'proyecto':proyecto},
                                                      context_instance=RequestContext(request))
                        else:
                            flujo_form.save()
                            return render_to_response('flujos/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                else:
                    if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                        mensaje=3
                        return render_to_response('flujos/editar_flujo.html', { 'form': flujo_form,'mensaje':mensaje, 'flujo': flujo, 'proyecto':proyecto},
                                                  context_instance=RequestContext(request))
                    else:
                        flujo_form.save()
                        return render_to_response('flujos/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        # formulario inicial
        flujo_form = ModificarFlujoForm(instance=flujo)
    return render_to_response('flujos/editar_flujo.html', { 'form': flujo_form, 'flujo': flujo, 'proyecto':proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('flujo')
def flujos_todas(request,id_proyecto):
    """
    vista para listar las flujos del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('flujos/flujos_todas.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))
    """
    flujos = Flujo.objects.all()
    proyecto = Proyecto.objects.get(id=id_proyecto)
    return render_to_response('flujos/flujos_todas.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('flujo')
def detalle_flujo(request, id_flujo):

    """
    Vista para ver los detalles del usuario <id_user> del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_flujo: referencia a la flujo dentro de la base de datos
    @return: render_to_response
    """

    dato = get_object_or_404(Flujo, pk=id_flujo)
    proyecto = Proyecto.objects.get(id=dato.proyecto_id)

    return render_to_response('flujos/detalle_flujo.html', {'datos': dato,'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('flujo')
def eliminar_flujo(request,id_flujo):
    """
    Vista para eliminar un flujo de un proyecto. Busca la flujo por su id_flujo y lo destruye.
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_flujo: referencia a la flujo dentro de la base de datos
    @return: render_to_response('flujos/listar_flujos.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))
    """
    flujo = get_object_or_404(Flujo, pk=id_flujo)
    proyecto = Proyecto.objects.get(id=flujo.proyecto_id)
    if proyecto.estado =='PRO':
        flujo.delete()
    flujos = Flujo.objects.filter(proyecto_id=proyecto.id).order_by('orden')
    return render_to_response('flujos/listar_flujos.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('flujo')
def buscar_flujos(request,id_proyecto):
    """
    vista para buscar los flujos del proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))
    """
    query = request.GET.get('q', '')
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if query:
        qset = (
            Q(nombre__contains=query)
        )
        results = Flujo.objects.filter(qset, proyecto_id=id_proyecto).distinct()
    else:
        results = []


    return render_to_response('flujos/listar_flujos.html', {'datos': results, 'proyecto' : proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('flujo')
def asignar_userStory(request,id_flujo):
    """
    Vista auxiliar para obtener un listado de usuarios para asociar a el flujo
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_flujo: referencia a la flujo dentro de la base de datos
    @return: render_to_response
    """
    mensaje = 0 # sin errores
    flujo=Flujo.objects.get(id=id_flujo)
    proyecto = Proyecto.objects.get(id=flujo.proyecto_id)
    actividad1 = Actividad.objects.filter(flujo_id = id_flujo, orden = 1)
    cantActividad = actividad1.count()
    if cantActividad == 0:
        flujos = Flujo.objects.filter(proyecto_id=proyecto.id).order_by('orden')
        mensaje = 100 # Debe crear actividades al flujo antes de asignarle User Stories
        return render_to_response('flujos/listar_flujos.html', {'datos': flujos, 'proyecto' : proyecto, 'mensaje': mensaje}, context_instance=RequestContext(request))
    userStories=UserStory.objects.filter(proyecto_id = flujo.proyecto)

    # roles=Group.objects.filter(flujo__id=id_flujo)
    # for rol in roles:       #Un usuario tiene un rol por flujo
    #     usuarios=usuarios.exclude(groups__id=rol.id)

    return render_to_response('flujos/asignar_userStories.html', {'userStories': userStories, 'flujo' : flujo,'proyecto':proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('flujo')
def asignar_userStoryFlujo(request, id_userStory, id_flujo):
    """
    Vista auxiliar para obtener un listado de usuarios para asociar a el flujo
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_flujo: referencia a la flujo dentro de la base de datos
    @return: render_to_response
    """

    flujo=Flujo.objects.get(id=id_flujo)
    userStory=UserStory.objects.get(id=id_userStory)
    userStory.estadoScrum = 1
    userStory.flujo_id = id_flujo
    actividad1 = Actividad.objects.get(flujo_id = id_flujo, orden = 1)
    userStory.actividad_id = actividad1.id
    userStory.save()
    mensaje = 100

    proyecto = Proyecto.objects.get(id=flujo.proyecto_id)
    userStories=UserStory.objects.filter(proyecto_id = flujo.proyecto)

    # roles=Group.objects.filter(flujo__id=id_flujo)
    # for rol in roles:       #Un usuario tiene un rol por flujo
    #     usuarios=usuarios.exclude(groups__id=rol.id)

    return render_to_response('flujos/asignar_userStories.html', {'userStories': userStories, 'flujo' : flujo,'proyecto':proyecto, 'mensaje' : mensaje}, context_instance=RequestContext(request))

@login_required
@permission_required('flujo')
def desasignar_userStoryFlujo(request, id_userStory, id_flujo):
    """
    Vista auxiliar para obtener un listado de usuarios para asociar a el flujo
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_flujo: referencia a la flujo dentro de la base de datos
    @return: render_to_response
    """

    flujo=Flujo.objects.get(id=id_flujo)
    userStory=UserStory.objects.get(id=id_userStory)
    userStory.estadoScrum = 0
    userStory.flujo_id = None
    userStory.actividad_id = None
    userStory.save()
    mensaje = 101

    proyecto = Proyecto.objects.get(id=flujo.proyecto_id)
    userStories=UserStory.objects.filter(proyecto_id = flujo.proyecto)

    # roles=Group.objects.filter(flujo__id=id_flujo)
    # for rol in roles:       #Un usuario tiene un rol por flujo
    #     usuarios=usuarios.exclude(groups__id=rol.id)

    return render_to_response('flujos/asignar_userStories.html', {'userStories': userStories, 'flujo' : flujo,'proyecto':proyecto, 'mensaje' : mensaje}, context_instance=RequestContext(request))


@login_required
@permission_required('flujo')
def desasignar_usuario(request,id_flujo):
    """
    vista para listar a los usuario de un flujo, para poder desasociarlos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_flujo: referencia a la flujo dentro de la base de datos
    @return: render_to_response('flujos/desasignar_usuarios.html', {'datos': usuarios,'flujo':id_flujo,'proyecto':proyecto}, context_instance=RequestContext(request))
    """
    flujo=Flujo.objects.get(id=id_flujo)
    proyecto = Proyecto.objects.get(id=flujo.proyecto_id)
    if proyecto.estado!='PRO':
        proyectos = Proyecto.objects.all().exclude(estado='ELI')
        return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos,'mensaje':1},
                              context_instance=RequestContext(request))
    roles=Group.objects.filter(flujo__id=id_flujo)
    usuarios=[]
    for rol in roles:
        p=User.objects.filter(groups__id=rol.id)
        for pp in p:
            usuarios.append(pp) #lista todos los usuarios con rol en el flujo
    return render_to_response('flujos/desasignar_usuarios.html', {'datos': usuarios,'flujo':flujo,'proyecto':proyecto,'roles':roles}, context_instance=RequestContext(request))

@login_required
@permission_required('proyectos')
def estadoKanban(request, id_flujo):
    """

    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/cambiar_estado_proyecto.html', { 'proyectos': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))
    """
    # formulario inicial
    # flujo=Flujo.objects.get(id=id_flujo)
    userStories = UserStory.objects.filter(flujo=id_flujo)
    actividades = Actividad.objects.filter(flujo_id=id_flujo)
    cantActividades = actividades.count()
    print "cantactividades"
    print cantActividades
    return render_to_response('flujos/kanban.html', {'userStories': userStories, 'actividades': actividades, 'cantActividades': cantActividades}, context_instance=RequestContext(request))