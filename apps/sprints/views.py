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
from apps.sprints.forms import ReasignarSprint, CrearSprintForm
#from apps.roles.forms import GroupForm
from datetime import datetime, timedelta
from django.contrib.auth.models import User, Group
from django.utils.timezone import utc
from apps.flujos.models import Flujo
from django.forms import formset_factory
from django.utils import timezone
from apps.trabajos.models import Trabajo
from apps.actividades.models import Actividad

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

    #Desasignar los User Stories asignados a ese sprint antes de eliminar
    USNoTerminados = UserStory.objects.filter(sprint_id = id_sprint)
    mensaje = ""
    if USNoTerminados.count() > 0:
        #borrar el id a este sprint de todos los user stories que lo tengas y no esten finalizados
        mensaje = "Los User Stories asignados fueron devueltos al BackLog"
        for userS in USNoTerminados:
            userS.sprint_id = None
            userS.save()

    sprint = Sprint.objects.get(id = id_sprint)

    #borrar el sprint
    sprint.delete()

    sprints = Sprint.objects.filter(proyecto_id=sprint.proyecto_id).order_by('orden')

    haySprintActivo = Sprint.objects.filter(proyecto_id=sprint.proyecto_id, estado = 1)

    return render_to_response('sprints/listar_sprints.html', {'datos': sprints, 'proyecto' : proyecto, 'sprintActivo': haySprintActivo.count(), 'mensaje': mensaje}, context_instance=RequestContext(request))



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
    proyecto = Proyecto.objects.get(id=sprint.proyecto_id)

    if proyecto.estado != "PRO":
        mensaje = 'El Sprint no puede iniciar si el proyecto no se encuentra en Produccion'
    else:
        mensaje = None
        sprint.estado = 1
        sprint.inicio = datetime.now()
        sprint.save()

    sprints = Sprint.objects.filter(proyecto_id=sprint.proyecto_id).order_by('orden')

    haySprintActivo = Sprint.objects.filter(proyecto_id=sprint.proyecto_id, estado = 1)

    return render_to_response('sprints/listar_sprints.html', {'datos': sprints, 'proyecto' : proyecto, 'sprintActivo': haySprintActivo.count(), 'mensaje': mensaje}, context_instance=RequestContext(request))

@login_required
@permission_required('sprint')
def finalizar_sprint(request, id_sprint):
    """
    vista para iniciar el sprint
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))
    """
    print "entro"
    sprint = Sprint.objects.get(id = id_sprint)
    sprint.estado = 2
    sprint.fin = datetime.now()
    sprint.save()

    proyecto = Proyecto.objects.get(id=sprint.proyecto_id)
    USNoTerminados = UserStory.objects.filter(sprint_id = id_sprint).exclude(estadoKanban = 4)
    if USNoTerminados.count() > 0:
        #borrar el id a este sprint de todos los user stories que lo tengas y no esten finalizados
        # for userS in USNoTerminados:
        #     userS.sprint_id = None
        #     userS.save()

        return render_to_response('sprints/sprintF_USNoTerminados.html', {'USNoTerminados': USNoTerminados, 'proyecto' : proyecto, 'sprint': sprint}, context_instance=RequestContext(request))
    else:
        sprints = Sprint.objects.filter(proyecto_id=sprint.proyecto_id).order_by('orden')

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
def asignar_userStorySprint(request, id_userStory, id_sprint):
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
        actividad1 = Actividad.objects.get(flujo_id = userStory.flujo_id, orden = 1)
        userStory.actividad_id = actividad1.id
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
        formulario = AsignarFlujoDesarrollador(request.POST, id_proyecto=proyecto.id)
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
    userStory.actividad_id = None
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


@login_required
@permission_required('sprint')
def reasignar_userStorySprint(request, id_userStory):
    """
    Vista para eliminar un sprint de un proyecto. Busca la sprint por su id_sprint y lo destruye.
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_sprint: referencia a la flujo dentro de la base de datos
    @return: render_to_response('sprints/listar_sprints.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))
    """
    userStory = UserStory.objects.get(id = id_userStory)
    sprintViejo = get_object_or_404(Sprint, pk=userStory.sprint_id)
    proyecto = Proyecto.objects.get(id=sprintViejo.proyecto_id)

    if request.method == 'POST':

        userStory.sprint_id = request.POST["sprint"]
        userStory.save()


        equipo = MiembroEquipo.objects.filter(proyecto_id = proyecto.id, usuario_id = userStory.desarrollador)
        horasPorDia = 0
        for equipi in equipo:
            horasPorDia = equipi.horasPorDia

        # anhadir la capacidad al sprint
        #anhadir horasUS .. tiempo estimado
        sprint = Sprint.objects.get(id = userStory.sprint_id)
        timediff = sprint.fin_propuesto - sprint.inicio_propuesto

        sprint.horasUS = sprint.horasUS + userStory.tiempo_estimado - userStory.tiempo_registrado
        sprint.capacidad = sprint.capacidad + (horasPorDia * timediff.days)
        sprint.save()

        USNoTerminados = UserStory.objects.filter(sprint_id = sprintViejo.id).exclude(estadoKanban = 4)
        if USNoTerminados.count() > 0:
            return render_to_response('sprints/sprintF_USNoTerminados.html', {'USNoTerminados': USNoTerminados, 'proyecto' : proyecto, 'sprint': sprint}, context_instance=RequestContext(request))
        else:
            sprints = Sprint.objects.filter(proyecto_id=sprint.proyecto_id).order_by('orden')

            haySprintActivo = Sprint.objects.filter(proyecto_id=sprint.proyecto_id, estado = 1)

            return render_to_response('sprints/listar_sprints.html', {'datos': sprints, 'proyecto' : proyecto, 'sprintActivo': haySprintActivo.count()}, context_instance=RequestContext(request))


    else:
        formulario = ReasignarSprint(proyecto.id)
        return render_to_response('sprints/reasignar_Sprint.html', { 'formulario': formulario, 'proyecto':proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('sprint')
def US_no_reasignar(request, id_sprint):
    """
    Vista para eliminar un sprint de un proyecto. Busca la sprint por su id_sprint y lo destruye.
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_sprint: referencia a la flujo dentro de la base de datos
    @return: render_to_response('sprints/listar_sprints.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))
    """
    USNoTerminados = UserStory.objects.filter(sprint_id = id_sprint).exclude(estadoKanban = 4)
    if USNoTerminados.count() > 0:
        #borrar el id a este sprint de todos los user stories que lo tengas y no esten finalizados
        for userS in USNoTerminados:
            userS.sprint_id = None
            userS.save()

    sprint = Sprint.objects.get(id = id_sprint)
    proyecto = Proyecto.objects.get(id=sprint.proyecto_id)
    sprints = Sprint.objects.filter(proyecto_id=sprint.proyecto_id).order_by('orden')
    haySprintActivo = Sprint.objects.filter(proyecto_id=sprint.proyecto_id, estado = 1)
    return render_to_response('sprints/listar_sprints.html', {'datos': sprints, 'proyecto' : proyecto, 'sprintActivo': haySprintActivo.count()}, context_instance=RequestContext(request))


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


@login_required
@permission_required('sprint')
def graficar(request, id_sprint):
    sprint = Sprint.objects.get(id = id_sprint)
    hs_total = sprint.capacidad
    diasIdeales = sprint.fin_propuesto - sprint.inicio_propuesto
    hs_dia = hs_total / diasIdeales.days
    listHsIdeal = []

    #today = timezone.now()
    listTaskHs = []
    diagrap = sprint.inicio
    #print diagrap
    #print listLab
    hoy = timezone.now().date()
    if hoy <= sprint.fin_propuesto:

        for ind in range(diasIdeales.days):
            hs_total = hs_total - hs_dia
            listHsIdeal.append(hs_total)
        diasLab = 0
        listLab = []
        diasCompleto = sprint.fin_propuesto - sprint.inicio_propuesto
        for ind in range(diasCompleto.days):
            diasLab = diasLab + 1
            #condias = 'Dia ' +  str(diasLab)
            listLab.append(diasLab)
        dayLimite = hoy - sprint.inicio
        capSpring = sprint.capacidad
        for dia in range(dayLimite.days):
            usList = UserStory.objects.filter(sprint_id = id_sprint)
            for us in usList:
                taskList = Trabajo.objects.filter(userStory_id = us.id)
                taskHs = 0
                notrab = 0
                for tsk in taskList:
                    if diagrap == tsk.fecha:
                        taskHs =  taskHs + tsk.hora
                        notrab = notrab + 1
                capSpring = capSpring - taskHs
                listTaskHs.append(capSpring)
                diagrap = diagrap + timedelta(days=1)
            #print listTaskHs

    elif hoy > sprint.fin:
        #print "emtro aca en el elif"
        #print sprint.id
        #print id_sprint
        for ind in range(diasIdeales.days):
            hs_total = hs_total - hs_dia
            listHsIdeal.append(hs_total)
        diasLab = 0
        listLab = []
        diasCompleto = sprint.fin - sprint.inicio_propuesto
        for ind in range(diasCompleto.days):
            diasLab = diasLab + 1
            #condias = 'Dia ' +  str(diasLab)
            listLab.append(diasLab)
        dayLimite = sprint.fin - sprint.inicio
        #print dayLimite
        capSpring = sprint.capacidad
        for dia in range(dayLimite.days):
            usList = UserStory.objects.filter(sprint_id = id_sprint)
            #print usList
            for us in usList:
                #print us.id
                taskList = Trabajo.objects.filter(userStory_id = us.id)
                taskHs = 0
                notrab = 0
                for tsk in taskList:

                    if diagrap == tsk.fecha:
                        print diagrap
                        taskHs =  taskHs + tsk.hora
                        notrab = notrab + 1
                capSpring = capSpring - taskHs
                if capSpring < 0:
                    capSpring = 0
                    listTaskHs.append(capSpring)
                    diagrap = diagrap + timedelta(days=1)
                elif capSpring != 0:
                    listTaskHs.append(capSpring)
                    diagrap = diagrap + timedelta(days=1)
        print listTaskHs
        print listHsIdeal

    return render_to_response('sprints/burndown_chart.html', {'listHsIdeal':listHsIdeal, 'listLab':listLab, 'listTaskHs':listTaskHs},
                          context_instance=RequestContext(request))


@login_required
@permission_required('sprint')
def sprintF_USNoTerminados(request, id_sprint):
    sprint = Sprint.objects.get(id = id_sprint)
    proyecto = Proyecto.objects.get(id=sprint.proyecto_id)
    USNoTerminados = UserStory.objects.filter(sprint_id = id_sprint).exclude(estadoKanban = 4)
    return render_to_response('sprints/sprintF_USNoTerminados.html', {'USNoTerminados': USNoTerminados, 'proyecto' : proyecto, 'sprint': sprint}, context_instance=RequestContext(request))


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
#     #  si todavia no termino el sprint, se muestra hasta hoy o hasta el fin de sprint?
#     today = timezone.now().date()
#
#     fin = today if today < sprint.fin else sprint.fin
#     db_hwork = [0]
#     for dia in daterange(sprint.inicio, sprint.fin):
#         #notas = trabajo_set.filter(fecha__year=dia.year, fecha__month=dia.month, fecha__day=dia.day)
#         #completados = notas.filter(estado=3).count()  # User Stories terminados en el dia
#         #hwork = notas.aggregate(sum=Sum('horas_a_registrar'))['sum']  # Total de horas registradas en el dia
#         #hwork = hwork if hwork else 0  # Por si aggregate devuelve None
#         # controlar si se registran mas horas de lo estimado
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