from django.shortcuts import render
from apps.actividades.models import Actividad
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from apps.userStories.models import UserStory
from apps.trabajos.models import Trabajo, Adjunto
from apps.trabajos.forms import crearTrabajoForm, NuevoAdjunto
from datetime import date
from apps.equipos.models import MiembroEquipo
from apps.proyectos.models import Proyecto
from apps.flujos.models import Flujo
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect
from base64 import b64encode

# Create your views here.
# @login_required
# @permission_required('userStories, trabajos')
# def listar_trabajos(request,id_userStory):
#     """
#     vista para listar las actividades de los flujos
#     @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
#     @return render_to_response('flujos/listar_flujos.html', {'datos': flujos}, context_instance=RequestContext(request))
#     """
#     trabajo = Trabajo.objects.filter(id=id_userStory)
#     userStory = UserStory.objects.get(id=id_userStory)
#     if userStory.estadoScrum!=0:
#         userStories = UserStory.objects.all().exclude(estadoScrum=3)
#         return render_to_response('userStories/listar_userStories.html', {'datos': userStories,'mensaje':1},
#                               context_instance=RequestContext(request))
#     else:
#         return render_to_response('trabajos/listar_trabajos.html', {'datos': trabajo}, context_instance=RequestContext(request))



@login_required
def listar_trabajos(request,id_userStory):
    """
    vista para listar los trabajos pertenecientes a un user story
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_userStory: clave foranea a la flujo
    @return render_to_response(..) o HttpResponse(...)
    """
    #tuserStory=get_object_or_404(Flujo,id=id_flujo)
    #flujo=Flujo.objects.filter(id=id_flujo)
    #if es_miembro(request.user.id,flujo,''):
    trabajos=Trabajo.objects.filter(userStory_id = id_userStory)
    #if puede_add_userStories(flujo):
    # nivel = 3
    #id_proyecto=Flujo.objects.get().proyecto_id
    #proyecto=Proyecto.objects.get(pk=UserStory.proyecto)
    return render_to_response('trabajos/listar_trabajos.html', {'datos': trabajos},
                                  context_instance=RequestContext(request))


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
        #userStory_id = UserStory.objects.get(id=id_userStory)
        formulario = crearTrabajoForm(request.POST)

        if formulario.is_valid():
            #today = datetime.now() #fecha actual
            #dateFormat = today.strftime("%Y-%m-%d") # fecha con format
            #obtener item con el cual relacionar
            #item_nombre=request.POST.get('entradalista')

            newTrabajo=Trabajo(descripcion=request.POST['descripcion'], tipo_trabajo=request.POST['tipo_trabajo'],hora=request.POST['hora'], fecha=date, userstory_id=request.POST['userstory'],
                               sprint_id=request.POST['sprint'])
            newTrabajo.save()

            # enviar correo de notificacion al scrum master
            proyecto = newTrabajo.userstory.proyecto
            id_proyecto = proyecto.id
            rolSM = Group.objects.filter(name = "Scrum Master")
            equipi = MiembroEquipo.objects.get(rol = rolSM, proyecto_id = id_proyecto)
            SM = equipi.usuario
            correo = SM.email
            send_mail("Asunto", "Mensaje del sistema. \n\nSe ha creado un nuevo Trabajo en el user story '" + newTrabajo.userstory.nombre + "'",
                      '"SIGEPRO" <sigepro-is2@gmail.com>',[correo])

            #guardar archivo

                #guardar atributos
        return render_to_response('trabajos/creacion_correcta.html',{}, context_instance=RequestContext(request))
    else:

        formulario = crearTrabajoForm()
        hijo=False
        #proyecto=Proyecto.objects.filter(id=flujo.proyecto_id)
        return render_to_response('trabajos/crear_trabajos.html', { 'formulario': formulario}, context_instance=RequestContext(request))


def upload_listar(request, id_trabajo):
    trabajo = Trabajo.objects.get(id = id_trabajo)
    if request.method == 'POST':
        adjunto = Adjunto(nombre=request.POST['nombre'], descripcion=request.POST['descripcion'], binario=request.read(), trabajo_id=id_trabajo)
        adjunto.save()
        return render_to_response('trabajos/listar_trabajos.html', {'datos': trabajo},
                                  context_instance=RequestContext(request))
    else:
        hayAdjunto = Adjunto.objects.filter(trabajo_id = id_trabajo)
        userStory = UserStory.objects.get(id = trabajo.userStory_id)
        flujo = Flujo.objects.get(id = userStory.flujo_id)
        proyecto = Proyecto.objects.get(id = userStory.proyecto_id)
        if hayAdjunto.count() == 0: # si no hay adjuntos.. muestra el template para cargar
            formulario = NuevoAdjunto()
            return render_to_response('trabajos/adjunto.html',{'id_trabajo': id_trabajo, 'formulario': formulario, 'proyecto': proyecto, 'flujo': flujo}, context_instance = RequestContext(request))
        else: # muestra el adjunto
            adjunto = Adjunto.objects.get(trabajo_id = id_trabajo)
            return render_to_response('trabajos/ver_adjunto.html',{'id_trabajo': id_trabajo, 'proyecto': proyecto, 'flujo': flujo, 'adjunto': adjunto}, context_instance = RequestContext(request))



def upload_handler(request, attachment, uploaded_file):
        #attachment.user_story = self.user_story
        attachment.nombre = uploaded_file.name


        attachment.content_type = uploaded_file.content_type
        attachment.binario = uploaded_file.read()
        attachment.save()
        return render_to_response('trabajos/adjuntar.html',{},context_instance = RequestContext(request))

# def form_valid(self, form):
#         attachment = form.save(commit=False)
#         self.upload_handler(attachment, self.request.FILES['file'])
#         return HttpResponseRedirect(attachment.get_absolute_url())