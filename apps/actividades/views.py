from django.shortcuts import render
from apps.flujos.models import Flujo
from apps.actividades.models import Actividad
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
# Create your views here.


@login_required
@permission_required('flujos, actividades')
def listar_actividades(request,id_flujo):
    """
    vista para listar las actividades de los flujos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('flujos/listar_flujos.html', {'datos': flujos}, context_instance=RequestContext(request))
    """
    actividades = Actividad.objects.filter(proyecto_id=id_flujo).order_by('orden')
    flujo = Flujo.objects.get(id=id_flujo)
    if flujo.estado!='PEN':
        flujos = Flujo.objects.all().exclude(estado='ELI')
        return render_to_response('flujos/listar_flujos.html', {'datos': flujos,'mensaje':1},
                              context_instance=RequestContext(request))
    else:
        return render_to_response('actividades/listar_actividades.html', {'datos': actividades}, context_instance=RequestContext(request))