from django.contrib.auth.decorators import login_required, permission_required
#from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.sprints.models import Sprint
#from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q
#from django.contrib import messages
#from sigepro import settings
#from django.contrib import messages
#from django.shortcuts import render
from apps.proyectos.models import Proyecto
from apps.sprints.forms import SprintForm, CrearSprintForm
#from apps.roles.forms import GroupForm
from datetime import datetime, timedelta

# Create your views here.


@login_required
@permission_required('proyectos, sprints')
def listar_sprints(request,id_proyecto):
    """
    vista para listar los sprints del proyectos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('sprints/listar_sprints.html', {'datos': sprints}, context_instance=RequestContext(request))
    """
    sprints = Sprint.objects.filter(proyecto_id=id_proyecto).order_by('orden')
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if proyecto.estado!='PRO':
        proyectos = Proyecto.objects.all().exclude(estado='ELI')
        return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos,'mensaje':1},
                              context_instance=RequestContext(request))
    else:
        return render_to_response('sprints/listar_sprints.html', {'datos': sprints, 'proyecto' : proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('sprint')
def registrar_sprint(request, id_proyecto):
    """
    Vista para registrar un nuevo sprint dentro de proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return HttpResponseRedirect('/sprints/register/success') si el rol fue correctamente asignado o
    render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request)) al formulario
    """
    mensaje=100
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if request.method=='POST':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        formulario = CrearSprintForm(request.POST)
        if formulario.is_valid():
            newSprint = Sprint(nombre = request.POST["nombre"], proyecto_id = id_proyecto, descripcion = request.POST["descripcion"])

            orden = Sprint.objects.filter(proyecto_id=id_proyecto)
            cantidad = orden.count()
            if cantidad>0: # comprobaciones de fecha
                newSprint.orden=orden.count()+1 #Calculo del orden del sprint a crear
            else:
                newSprint.orden=1
            newSprint.save()
            return render_to_response('sprints/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = CrearSprintForm() #formulario inicial
    return render_to_response('sprints/registrar_sprints.html',{'formulario':formulario,'id':id_proyecto, 'proyecto':proyecto, 'mensaje':mensaje},
                              context_instance=RequestContext(request))


@login_required
@permission_required('sprint')
def eliminar_sprint(request,id_sprint):
    """
    Vista para eliminar un sprint de un proyecto. Busca la sprint por su id_sprint y lo destruye.
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_sprint: referencia a la flujo dentro de la base de datos
    @return: render_to_response('sprints/listar_sprints.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))
    """
    sprint = get_object_or_404(Sprint, pk=id_sprint)
    proyecto = Proyecto.objects.get(id=sprint.proyecto_id)
    if proyecto.estado =='PRO':
        sprint.delete()
    sprints = Sprint.objects.filter(proyecto_id=proyecto.id).order_by('orden')
    return render_to_response('sprints/listar_sprints.html', {'datos': sprints, 'proyecto' : proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('sprint')
def buscar_sprints(request,id_proyecto):
    """
    vista para buscar los sprints del proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))
    """
    query = request.GET.get('q', '')
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if query:
        qset = (
            Q(nombre__contains=query)
        )
        results = Sprint.objects.filter(qset, proyecto_id=id_proyecto).distinct()
    else:
        results = []


    return render_to_response('sprints/listar_sprints.html', {'datos': results, 'proyecto' : proyecto}, context_instance=RequestContext(request))


