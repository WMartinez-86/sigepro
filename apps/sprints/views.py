from django.contrib.auth.decorators import login_required, permission_required
#from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.sprints.models import Sprint
#from django.contrib.auth.models import User, Group, Permission
#from django.db.models import Q
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
    sprints = Sprint.objects.filter(id=id_proyecto).order_by('inicio')
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
            if len(str(request.POST["inicio"])) != 10 : #Comprobacion de formato de fecha
                mensaje=0
                return render_to_response('sprints/registrar_sprints.html',{'formulario':formulario,'mensaje':mensaje,'id':id_proyecto}, context_instance=RequestContext(request))
            else:
                fecha=datetime.strptime(str(request.POST["inicio"]),'%d/%m/%Y')
                fecha=fecha.strftime('%Y-%m-%d')
                fecha1=datetime.strptime(fecha,'%Y-%m-%d')
                sprint_time = proyecto.duracion_sprint
                fechafin=fecha1 + timedelta(days=sprint_time)
                print (fechafin)

                newSprint = Sprint(nombre = request.POST["nombre"],
                               inicio = fecha, proyecto_id = id_proyecto, fin = fechafin)
                aux=0
                orden = Sprint.objects.filter(proyecto_id=id_proyecto)

                if aux>0:
                    aux=1
                else:
                    proyecto=Proyecto.objects.get(id=id_proyecto)
                    cantidad = orden.count()
                    if cantidad>0:#comprobaciones de fecha
                       anterior = Sprint.objects.get(orden=cantidad, proyecto_id=id_proyecto)
                       if fecha1<datetime.strptime(str(anterior.inicio),'%Y-%m-%d'):
                           #Fecha de inicio no puede ser menor a la fecha de fin del sprint anterior
                           return render_to_response('sprints/registrar_sprints.html',{'formulario':formulario,'mensaje':1,'id':id_proyecto,'proyecto':proyecto},
                                                     context_instance=RequestContext(request))
                       else:
                            if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                                #Fecha de inicio no concuerda con proyecto
                                print(fecha1)
                                print(datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d'))
                                print (datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d'))
                                return render_to_response('sprints/registrar_sprints.html',{'formulario':formulario,'mensaje':2,'id':id_proyecto,'proyecto':proyecto},
                                                          context_instance=RequestContext(request))
                            else:
                                newSprint.orden=orden.count()+1 #Calculo del orden del sprint a crear
                                newSprint.save()
                                return render_to_response('sprints/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                    else:
                        newSprint.orden=1
                        newSprint.save()
                        return render_to_response('sprints/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = CrearSprintForm() #formulario inicial
    return render_to_response('sprints/registrar_sprints.html',{'formulario':formulario,'id':id_proyecto, 'proyecto':proyecto, 'mensaje':mensaje},
                              context_instance=RequestContext(request))
