from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from datetime import datetime

__text__ = 'Este modulo contiene funciones que permiten el control de proyectos'
# Create your views here.

@login_required
@permission_required('proyectos')
def listar_proyectos(request):
    """
    vista para listar los proyectos del sistema junto con el nombre de su cliente
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos}, context_instance=RequestContext(request))
    """
    #proyectos = Proyecto.objects.filter((Q(estado='PEN')|Q(estado='ANU')))
    proyectos = Proyecto.objects.all().exclude(estado='ELI')

    return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos,'mensaje':1000},
                              context_instance=RequestContext(request))
