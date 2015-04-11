from django.contrib.auth.decorators import login_required, permission_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from apps.proyectos.models import Proyecto
from django.views.generic import TemplateView, ListView
from django.utils import timezone
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect
from apps.proyectos.forms import ProyectoForm, CambiarEstadoForm

__text__ = 'Este modulo contiene funciones que permiten el control de proyectos'
# Create your views here.

# @login_required
# @permission_required('proyectos')
# def listar_proyectos(ListView):
#     """
#     vista para listar los proyectos del sistema junto con el nombre de su cliente
#     @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
#     @return: render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos}, context_instance=RequestContext(request))
#     """
#     #proyectos = Proyecto.objects.filter((Q(estado='PEN')|Q(estado='ANU')))
#     proyectos = Proyecto.objects.all().exclude(estado='ELI')
#
#     return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos,'mensaje':1000},
#                               context_instance=RequestContext(request))


class lista_proyectos(ListView):
    template_name = 'proyectos/listar_proyectos.html'
    model = Proyecto


@login_required
@permission_required('proyectos')
def registra_proyecto(request):
    """
    Vista para registrar un nuevo proyecto con su lider y miembros de su comite de cambios
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
                # lider = formulario.cleaned_data['lider']
                # #Eslider=Perfiles.objects.get(usuario=lider)
                # #Verifica si esta puede ser lider
                # if Eslider.lider != True:
                #     return render_to_response('proyectos/registrar_proyecto.html', {'formulario': formulario, 'mensaje': 2},
                #                           context_instance=RequestContext(request))
                # #asigna el rol lider al usuario seleccionado
                # roles = Group.objects.get(name='Lider')
                # lider.groups.add(roles)
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