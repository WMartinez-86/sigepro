from django.contrib.auth.decorators import login_required, permission_required
#from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from apps.sprints.models import Sprint
#from django.contrib.auth.models import User, Group, Permission
from django.db.models import Q, Sum
#from django.contrib import messages
#from sigepro import settings
#from django.contrib import messages
#from django.shortcuts import render
from apps.proyectos.models import Proyecto
from apps.equipos.models import MiembroEquipo
from apps.userStories.models import UserStory
from apps.sprints.forms import AsignarFlujoDesarrollador
from apps.sprints.forms import SprintForm, CrearSprintForm
#from apps.roles.forms import GroupForm
from datetime import datetime, timedelta
from django.contrib.auth.models import User, Group
from django.utils.timezone import utc
from apps.flujos.models import Flujo
from django.forms import formset_factory
from django.utils import timezone
from apps.trabajos.models import Trabajo

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
    haySprintActivo = Sprint.objects.filter(proyecto_id=id_proyecto, estado = 1)

    return render_to_response('sprints/listar_sprints.html', {'datos': sprints, 'proyecto' : proyecto, 'sprintActivo': haySprintActivo.count()}, context_instance=RequestContext(request))


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
            inicio_propuesto=datetime.strptime(str(request.POST["inicio_propuesto"]),'%d/%m/%Y')
            inicio_propuesto=inicio_propuesto.strftime('%Y-%m-%d')
            fecha1=datetime.strptime(inicio_propuesto,'%Y-%m-%d')

            fin_propuesto=datetime.strptime(str(request.POST["fin_propuesto"]),'%d/%m/%Y')
            fin_propuesto=fin_propuesto.strftime('%Y-%m-%d')
            fecha2=datetime.strptime(fin_propuesto,'%Y-%m-%d')

            newSprint = Sprint(nombre = request.POST["nombre"], proyecto_id = id_proyecto, descripcion = request.POST["descripcion"], inicio_propuesto = fecha1, fin_propuesto = fecha2)

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


@login_required
@permission_required('sprint')
def iniciar_sprint(request, id_sprint):
    """
    vista para iniciar el sprint
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))
    """
    sprint = Sprint.objects.get(id = id_sprint)
    sprint.estado = 1
    sprint.inicio = datetime.now()
    sprint.save()

    sprints = Sprint.objects.filter(proyecto_id=sprint.proyecto_id).order_by('orden')
    proyecto = Proyecto.objects.get(id=sprint.proyecto_id)
    haySprintActivo = Sprint.objects.filter(proyecto_id=sprint.proyecto_id, estado = 1)

    return render_to_response('sprints/listar_sprints.html', {'datos': sprints, 'proyecto' : proyecto, 'sprintActivo': haySprintActivo.count()}, context_instance=RequestContext(request))

@login_required
@permission_required('sprint')
def finalizar_sprint(request, id_sprint):
    """
    vista para iniciar el sprint
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))
    """
    sprint = Sprint.objects.get(id = id_sprint)
    sprint.estado = 2
    sprint.fin = datetime.now()
    sprint.save()

    sprints = Sprint.objects.filter(proyecto_id=sprint.proyecto_id).order_by('orden')
    proyecto = Proyecto.objects.get(id=sprint.proyecto_id)
    haySprintActivo = Sprint.objects.filter(proyecto_id=sprint.proyecto_id, estado = 1)

    return render_to_response('sprints/listar_sprints.html', {'datos': sprints, 'proyecto' : proyecto, 'sprintActivo': haySprintActivo.count()}, context_instance=RequestContext(request))


@login_required
@permission_required('sprint')
def listar_USSprintBacklog(request, id_sprint):
    """
    Vista para eliminar un sprint de un proyecto. Busca la sprint por su id_sprint y lo destruye.
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_sprint: referencia a la flujo dentro de la base de datos
    @return: render_to_response('sprints/listar_sprints.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))
    """
    sprint = get_object_or_404(Sprint, pk=id_sprint)
    proyecto = Proyecto.objects.get(id=sprint.proyecto_id)
    userStoriesBacklog = UserStory.objects.filter(sprint_id = None, proyecto_id = proyecto.id)
    userStoriesAsignados = UserStory.objects.filter(sprint_id = id_sprint, proyecto_id = proyecto.id)


    return render_to_response('sprints/asignar_userStories.html', {'userStoriesBacklog': userStoriesBacklog, 'userStoriesAsignados': userStoriesAsignados, 'sprint' : sprint,'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('sprint')
def asignar_userStorySprint(request, id_userStory,  id_sprint):
    """
    Vista para eliminar un sprint de un proyecto. Busca la sprint por su id_sprint y lo destruye.
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_sprint: referencia a la flujo dentro de la base de datos
    @return: render_to_response('sprints/listar_sprints.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))
    """
    sprint = get_object_or_404(Sprint, pk=id_sprint)
    proyecto = Proyecto.objects.get(id=sprint.proyecto_id)

    if request.method == 'POST':
        userStory = UserStory.objects.get(id = id_userStory)
        userStory.sprint_id = id_sprint
        userStory.flujo_id = request.POST["flujo"]
        userStory.desarrollador_id = request.POST["desarrollador"]
        userStory.save()


        userStoriesBacklog = UserStory.objects.filter(sprint_id = None, proyecto_id = proyecto.id)
        userStoriesAsignados = UserStory.objects.filter(sprint_id = id_sprint, proyecto_id = proyecto.id)


        equipo = MiembroEquipo.objects.filter(proyecto_id = proyecto.id, usuario_id = userStory.desarrollador)
        horasPorDia = 0
        for equipi in equipo:
            horasPorDia = equipi.horasPorDia
            print(horasPorDia)

        # anhadir la capacidad al sprint
        #anhadir horasUS .. tiempo estimado
        timediff = sprint.fin_propuesto - sprint.inicio_propuesto

        sprint.horasUS = sprint.horasUS + userStory.tiempo_estimado
        sprint.capacidad = sprint.capacidad + (horasPorDia * timediff.days)
        sprint.save()

        return render_to_response('sprints/asignar_userStories.html', {'userStoriesBacklog': userStoriesBacklog, 'userStoriesAsignados': userStoriesAsignados, 'sprint' : sprint, 'proyecto':proyecto}, context_instance=RequestContext(request))

    else:
        formulario = AsignarFlujoDesarrollador(proyecto.id)
        return render_to_response('sprints/asignar_FlujoDesarrollador.html', { 'formulario': formulario, 'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('sprint')
def desasignar_userStorySprint(request, id_userStory,  id_sprint):
    """
    Vista para eliminar un sprint de un proyecto. Busca la sprint por su id_sprint y lo destruye.
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_sprint: referencia a la flujo dentro de la base de datos
    @return: render_to_response('sprints/listar_sprints.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))
    """
    userStory = UserStory.objects.get(id = id_userStory)
    userStory.sprint_id = None
    userStory.save()

    sprint = get_object_or_404(Sprint, pk=id_sprint)
    proyecto = Proyecto.objects.get(id=sprint.proyecto_id)
    userStoriesBacklog = UserStory.objects.filter(sprint_id = None, proyecto_id = proyecto.id)
    userStoriesAsignados = UserStory.objects.filter(sprint_id = id_sprint, proyecto_id = proyecto.id)

    equipo = MiembroEquipo.objects.filter(proyecto_id = proyecto.id, usuario_id = userStory.desarrollador)
    horasPorDia = 0
    for equipi in equipo:
        horasPorDia = equipi.horasPorDia
        print(horasPorDia)

    # anhadir la capacidad al sprint
    #anhadir horasUS .. tiempo estimado
    timediff = sprint.fin_propuesto - sprint.inicio_propuesto

    sprint.horasUS = sprint.horasUS - userStory.tiempo_estimado
    sprint.capacidad = sprint.capacidad - (horasPorDia * timediff.days)
    sprint.save()

    return render_to_response('sprints/asignar_userStories.html', {'userStoriesBacklog': userStoriesBacklog, 'userStoriesAsignados': userStoriesAsignados, 'sprint' : sprint,'proyecto':proyecto}, context_instance=RequestContext(request))



def graficar(request, id_sprint):
    sprint = Sprint.objects.get(id = id_sprint)
    hs_total = sprint.capacidad
    dias = sprint.fin_propuesto - sprint.inicio_propuesto
    hs_dia = hs_total / dias.days

    print hs_total
    print hs_dia
    list = []
    for ind in range(dias.days):
        hs_total = hs_total - hs_dia
        list.append(hs_total)
    diasLab = 0
    listLab = []
    print list

    for ind in range(dias.days):
        diasLab = diasLab + 1
        listLab.append(diasLab)

    print listLab
    return render_to_response('sprints/burndown_chart.html', {'list':list, 'listLab':listLab},
                              context_instance=RequestContext(request))




# def get_sprint_burndown(request, id_sprint):
#     sprint = Sprint.objects.get(id = id_sprint)
#     project = sprint.proyecto_id
#     us = UserStory.objects.get(proyecto_id = project)
#     trabajo = Trabajo.objects.get(userStory_id = us.id)
#
#     total = sprint.userstory_set.aggregate(sum=Sum('tiempo_estimado'))['sum']
#     #print total
#     h_restante = h_total = total if total else 0 # Horas estimadas de US
#     lh_real = [h_total]  # Lista de horas registradas
#     lh_ideal = [h_total]  # Lista de horas reales
#
#     timediff = sprint.fin_propuesto - sprint.inicio_propuesto
#     duracion_sprint = timediff.days
#
#     m = float(h_total) / duracion_sprint  # Velocidad ideal
#     us_restante = us_total = sprint.userstory_set.count()  # User Stories del sprint
#     lus_restante = [us_total]  # Lista de user stories que faltan
#     lus_completado = [0]  # Lista de user stories que se terminaron
#     # TODO: si todavia no termino el sprint, se muestra hasta hoy o hasta el fin de sprint?
#     today = timezone.now().date()
#
#     fin = today if today < sprint.fin else sprint.fin
#     db_hwork = [0]
#     for dia in daterange(sprint.inicio, sprint.fin):
#         #notas = trabajo_set.filter(fecha__year=dia.year, fecha__month=dia.month, fecha__day=dia.day)
#         #completados = notas.filter(estado=3).count()  # User Stories terminados en el dia
#         #hwork = notas.aggregate(sum=Sum('horas_a_registrar'))['sum']  # Total de horas registradas en el dia
#         #hwork = hwork if hwork else 0  # Por si aggregate devuelve None
#         # TODO: controlar si se registran mas horas de lo estimado
#         #db_hwork.append(hwork)
#         #h_restante -= hwork if h_restante >= hwork else 0  # Si se terminan las horas antes del fin
#         h_total -= m
#         #us_restante -= completados
#         lh_real.append(h_restante)
#         lh_ideal.append(round(h_total, 1))
#         lus_restante.append(us_restante if us_restante > 0 else 0)
#         #lus_completado.append(completados)
#         #print lh_ideal
#
#     #return {'ideal': lh_ideal}
#     return render_to_response('sprints/burndown_chart.html', {'ideal': lh_ideal},
#                               context_instance=RequestContext(request))
#
#
# def daterange(start_date, end_date):
#    for n in range(int((end_date - start_date).days)):
#        yield start_date + timedelta(n)