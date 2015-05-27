from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User, Group
from apps.proyectos.models import Proyecto
from apps.proyectos.forms import ProyectoForm
from django.views.generic import TemplateView, ListView
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from apps.equipos.models import MiembroEquipo

from apps.flujos.models import Flujo
from django.contrib import messages
from sigepro import settings
from django.db.models import Q

__text__ = 'Este modulo contiene funciones que permiten el control de proyectos'
# Create your views here.

__author__ = 'juanma'

@login_required
@permission_required('proyectos')
def lista_proyectos(request):

    proyectos = Proyecto.objects.all()
    # proyecto = Proyecto.objects.get(id=id_proyecto)
    rolSM = Group.objects.filter(name = "Scrum Master")
    # equipos = MiembroEquipo.objects.filter(rol = rolSM)
    # equipos = MiembroEquipo.objects.filter()

    # haySM = MiembroEquipo.objects.filter(rol = rolSM, proyecto_id = miembro.proyecto_id)

    return render_to_response('proyectos/listar_proyectos.html', {'proyectos': proyectos, 'rolSM': rolSM},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def registra_proyecto(request):
    """
    Vista para registrar un nuevo proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return HttpResponseRedirect('/proyectos/register/success') si el rol lider fue correctamente asignado o
    render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request)) al formulario
    """

    if request.method == 'POST':
        formulario = ProyectoForm(request.POST)

        if formulario.is_valid():
            # fecha = datetime.strptime(str(request.POST["fecha_ini"]), '%d/%m/%Y')#convert string to datetime
            # fecha = fecha.strftime('%Y-%m-%d')# fecha con formato
            # fecha1 = datetime.strptime(fecha, '%Y-%m-%d')#convert string to datetime

            # fechaf = datetime.strptime(str(request.POST["fecha_fin"]), '%d/%m/%Y')#convert string to datetime
            # fechaf = fechaf.strftime('%Y-%m-%d')# fecha con formato
            # fecha2 = datetime.strptime(fechaf, '%Y-%m-%d') #convert string to datetime

            # fecha_actual = datetime.now() #fecha actual
            # fecha_actual = fecha_actual.strftime('%Y-%m-%d')#fecha con formato
            # if datetime.strptime(fecha_actual, '%Y-%m-%d') > fecha1:
            #     return render_to_response('proyectos/registrar_proyectos.html', {'formulario': formulario, 'mensaje': 1},
            #                               context_instance=RequestContext(request))
            # elif fecha1 > fecha2:
            #     return render_to_response('proyectos/registrar_proyectos.html', {'formulario': formulario, 'mensaje': 0},
            #                               context_instance=RequestContext(request))
            # else:

                formulario.save()
                return HttpResponseRedirect('/proyectos/register/success')
    else:
        formulario = ProyectoForm()
    return render_to_response('proyectos/registrar_proyectos.html', {'formulario': formulario, 'mensaje': 1000},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def RegisterSuccessView(request):
    """
    Vista llamada en caso de creacion correcta de un proyecto, redirige a un template de exito
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/creacion_correcta.html', context_instance=RequestContext(request))
    """
    return render_to_response('proyectos/creacion_correcta.html', context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def editar_proyecto(request, id_proyecto):
    """
    Vista para editar un proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: HttpResponseRedirect('/proyectos/register/success/') cuando el formulario es validado correctamente o render_to_response('proyectos/editar_proyecto.html', { 'proyectos': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    nombre = proyecto.nombre
    if request.method == 'POST':
        # formulario enviado
        proyecto_form = ProyectoForm(request.POST, instance=proyecto)
        if proyecto_form.is_valid():
            if proyecto_form.cleaned_data['fecha_ini'] > proyecto_form.cleaned_data['fecha_fin']:
                messages.add_message(request, settings.DELETE_MESSAGE,
                                     "Fecha de inicio debe ser menor a la fecha de finalizacion")
            else:

                # formulario validado correctamente
                proyecto_form.save()
                return HttpResponseRedirect('/proyectos/register/success/')
    else:
        # formulario inicial
        proyecto_form = ProyectoForm(instance=proyecto)
    return render_to_response('proyectos/editar_proyecto.html', {'proyectos': proyecto_form, 'nombre': nombre},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def buscar_proyecto(request):
    """
    vista para buscar los proyectos del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))
    """
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(nombre__contains=query)
        )
        results = Proyecto.objects.filter(qset).distinct()

    else:
        results = []

    return render_to_response('proyectos/listar_proyectos.html', {'proyectos': results},
                              context_instance=RequestContext(request))



@login_required
@permission_required('proyectos')
def detalle_proyecto(request, id_proyecto):
    """
    Vista para ver los detalles del proyecto del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato}, context_instance=RequestContext(request))
    """

    dato = get_object_or_404(Proyecto, pk=id_proyecto)
    return render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato},
                              context_instance=RequestContext(request))


# cambio de estado de proyecto

@login_required
@permission_required('proyectos')
def proyecto_iniciar(request, id_proyecto):
    """
    Vista para ver los detalles del proyecto del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato}, context_instance=RequestContext(request))
    """
    rolSM = Group.objects.filter(name = "Scrum Master")
    equipi = MiembroEquipo.objects.filter(rol = rolSM, proyecto_id = id_proyecto)
    if equipi.count() == 0:
        mensaje = 102 # no puede iniciar el proyecto sin asignar Scrum Master al equipo
        proyectos = Proyecto.objects.all()
        # proyecto = Proyecto.objects.get(id=id_proyecto)
        rolSM = Group.objects.filter(name = "Scrum Master")
        equipos = MiembroEquipo.objects.filter(rol = rolSM)
        return render_to_response('proyectos/listar_proyectos.html', {'proyectos': proyectos, 'mensaje': mensaje}, context_instance=RequestContext(request))
    else:
        proyectos = Proyecto.objects.get(id=id_proyecto)
        proyectos.estado = "PRO"
        proyectos.fecha_ini = datetime.now()
        proyectos.save()

        # listar proyectos
        proyectos = Proyecto.objects.all()
        return render_to_response('proyectos/listar_proyectos.html', {'proyectos': proyectos},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def proyecto_finalizar(request, id_proyecto):
    """
    Vista para ver los detalles del proyecto del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato}, context_instance=RequestContext(request))
    """
    proyectos = Proyecto.objects.get(id=id_proyecto)
    proyectos.estado = "FIN"
    proyectos.fecha_fin = datetime.now()
    proyectos.save()

    # listar proyectos
    proyectos = Proyecto.objects.all()
    return render_to_response('proyectos/listar_proyectos.html', {'proyectos': proyectos},
                          context_instance=RequestContext(request))

@login_required
@permission_required('proyectos')
def proyecto_aprobar(request, id_proyecto):
    """
    Vista para ver los detalles del proyecto del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato}, context_instance=RequestContext(request))
    """
    proyectos = Proyecto.objects.get(id=id_proyecto)
    proyectos.estado = "APR"
    proyectos.fecha_apr = datetime.now()
    proyectos.save()

    # listar proyectos
    proyectos = Proyecto.objects.all()
    return render_to_response('proyectos/listar_proyectos.html', {'proyectos': proyectos},
                          context_instance=RequestContext(request))

@login_required
@permission_required('proyectos')
def proyecto_eliminar(request, id_proyecto):
    """
    Vista para ver los detalles del proyecto del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato}, context_instance=RequestContext(request))
    """
    proyectos = Proyecto.objects.get(id=id_proyecto)
    proyectos.estado = "ELI"
    proyectos.fecha_eli = datetime.now()
    proyectos.save()

    # listar proyectos
    proyectos = Proyecto.objects.all()
    return render_to_response('proyectos/listar_proyectos.html', {'proyectos': proyectos},
                          context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def proyecto_rechazar(request, id_proyecto):
    """
    Vista para ver los detalles del proyecto del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato}, context_instance=RequestContext(request))
    """
    proyectos = Proyecto.objects.get(id=id_proyecto)
    proyectos.estado = "PRO"
    proyectos.fecha_fin = None
    proyectos.save()

    # listar proyectos
    proyectos = Proyecto.objects.all()
    return render_to_response('proyectos/listar_proyectos.html', {'proyectos': proyectos},
                          context_instance=RequestContext(request))