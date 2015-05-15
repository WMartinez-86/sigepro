from django.shortcuts import render
from apps.actividades.models import Actividad
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.userStories.models import UserStory
from apps.trabajos.models import Trabajo

# Create your views here.
@login_required
@permission_required('userStories, trabajos')
def listar_trabajos(request,id_userStory):
    """
    vista para listar las actividades de los flujos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('flujos/listar_flujos.html', {'datos': flujos}, context_instance=RequestContext(request))
    """
    trabajos = Trabajo.objects.filter(id=id_userStory)
    userStory = UserStory.objects.get(id=id_userStory)
    # if userStory.estado!='PEN':
    #     userStories = UserStory.objects.all().exclude(estado='ELI')
    #     return render_to_response('userStories/listar_userStories.html', {'datos': userStories,'mensaje':1},
    #                           context_instance=RequestContext(request))
    #else:
    return render_to_response('trabajos/listar_trabajos.html', {'datos': trabajos}, context_instance=RequestContext(request))