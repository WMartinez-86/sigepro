from django.shortcuts import render
from apps.actividades.models import Actividad
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.userStories.models import UserStory
from apps.trabajos.models import Trabajo
from apps.trabajos.forms import crearTrabajoForm

# Create your views here.
@login_required
@permission_required('userStories, trabajos')
def listar_trabajos(request,id_userStory):
    """
    vista para listar las actividades de los flujos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('flujos/listar_flujos.html', {'datos': flujos}, context_instance=RequestContext(request))
    """
    trabajo = Trabajo.objects.filter(id=id_userStory)
    userStory = UserStory.objects.get(id=id_userStory)
    # if userStory.estado!='PEN':
    #     userStories = UserStory.objects.all().exclude(estado='ELI')
    #     return render_to_response('userStories/listar_userStories.html', {'datos': userStories,'mensaje':1},
    #                           context_instance=RequestContext(request))
    #else:
    return render_to_response('trabajos/listar_trabajos.html', {'datos': trabajo}, context_instance=RequestContext(request))



def crear_trabajo(request):
    """
    Vista para crear un user story. Ademas se dan las opciones de agregar un
    archivo al item, y de completar todos los atributos de su tipo de item
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_tipoItem: clave foranea al tipoItem
    @ return render_to_response('items/...) o render_to_response('403.html')
    """

    if request.method=='POST':
        #formset = ItemFormSet(request.POST)
        formulario = crearTrabajoForm(request.POST)

        if formulario.is_valid():
            #today = datetime.now() #fecha actual
            #dateFormat = today.strftime("%Y-%m-%d") # fecha con format
            #obtener item con el cual relacionar
            #item_nombre=request.POST.get('entradalista')

            newTrabajo=Trabajo(descripcion=request.POST['descripcion'])
            newTrabajo.save()
            #guardar archivo

            #guardar atributos
        return render_to_response('trabajos/creacion_correcta.html',{}, context_instance=RequestContext(request))
    else:

        formulario = crearTrabajoForm()
        hijo=False
        #proyecto=Proyecto.objects.filter(id=flujo.proyecto_id)
        return render_to_response('trabajos/crear_trabajos.html', { 'formulario': formulario}, context_instance=RequestContext(request))

