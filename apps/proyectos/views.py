from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from apps.proyectos.models import Proyecto
from django.views.generic import TemplateView, ListView
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from apps.proyectos.forms import ProyectoForm, CambiarEstadoForm

from apps.flujos.models import Flujo
from django.contrib import messages
from sigepro import settings
from django.db.models import Q

__text__ = 'Este modulo contiene funciones que permiten el control de proyectos'
# Create your views here.

__author__ = 'juanma'


class lista_proyectos(ListView):
    template_name = 'proyectos/listar_proyectos.html'
    model = Proyecto


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
            fecha = datetime.strptime(str(request.POST["fecha_ini"]), '%d/%m/%Y')#convert string to datetime
            fecha = fecha.strftime('%Y-%m-%d')# fecha con formato
            fecha1 = datetime.strptime(fecha, '%Y-%m-%d')#convert string to datetime

            fechaf = datetime.strptime(str(request.POST["fecha_fin"]), '%d/%m/%Y')#convert string to datetime
            fechaf = fechaf.strftime('%Y-%m-%d')# fecha con formato
            fecha2 = datetime.strptime(fechaf, '%Y-%m-%d') #convert string to datetime

            fecha_actual = datetime.now() #fecha actual
            fecha_actual = fecha_actual.strftime('%Y-%m-%d')#fecha con formato
            if datetime.strptime(fecha_actual, '%Y-%m-%d') > fecha1:
                return render_to_response('proyectos/registrar_proyectos.html', {'formulario': formulario, 'mensaje': 1},
                                          context_instance=RequestContext(request))
            elif fecha1 > fecha2:
                return render_to_response('proyectos/registrar_proyectos.html', {'formulario': formulario, 'mensaje': 0},
                                          context_instance=RequestContext(request))
            else:

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
def cambiar_estado_proyecto(request, id_proyecto):
    """

    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/cambiar_estado_proyecto.html', { 'proyectos': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))
    """

    proyecto = Proyecto.objects.get(id=id_proyecto)
    nombre = proyecto.nombre
    if request.method == 'POST':
        proyecto_form = CambiarEstadoForm(request.POST, instance=proyecto)
        if proyecto_form.is_valid():
            if proyecto_form.cleaned_data['estado'] == 'PRO':

                # formulario validado correctamente
                proyecto_form.save()
                return HttpResponseRedirect('/proyectos/register/success/')
            else:
                if proyecto_form.cleaned_data['estado'] == 'ELI' or proyecto_form.cleaned_data['estado'] == 'PEN' or \
                                proyecto_form.cleaned_data['estado'] == 'ELI':
                    proyecto_form.save()
                    return HttpResponseRedirect('/proyectos/register/success/')

    else:
        # formulario inicial
        proyecto_form = CambiarEstadoForm(instance=proyecto)
        return render_to_response('proyectos/cambiar_estado_proyecto.html',
                                  {'proyectos': proyecto_form, 'nombre': nombre,'mensaje':1000}, context_instance=RequestContext(request))


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