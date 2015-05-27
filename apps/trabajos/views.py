from django.shortcuts import render
from apps.actividades.models import Actividad
from django.contrib.auth.decorators import login_required, permission_required, PermissionDenied
from django.shortcuts import render_to_response, get_object_or_404
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
from django.http import HttpResponseRedirect,HttpResponse
from base64 import b64encode
from datetime import datetime

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
    return render_to_response('trabajos/listar_trabajos.html', {'datos': trabajos, 'id_userStory': id_userStory},
                                  context_instance=RequestContext(request))


def crear_trabajo(request, id_userStory):
    """
    Vista para crear un trabajo. Ademas se dan las opciones de agregar un
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
            fecha=datetime.strptime(str(request.POST["fecha"]),'%d/%m/%Y')
            fechaCorreo=str(request.POST["fecha"]),'%d/%m/%Y'
            fecha=fecha.strftime('%Y-%m-%d')
            fecha1=datetime.strptime(fecha,'%Y-%m-%d')
            # obtener item con el cual relacionar
            item_nombre=request.POST.get('entradalista')

            newTrabajo=Trabajo(descripcion=request.POST['descripcion'],hora=request.POST['hora'], fecha=fecha1, userStory_id = id_userStory) #default tipo de trabajo es 0: normal
            newTrabajo.save()

            # enviar correo de notificacion al scrum master
            objdev = request.user
            desarrollador = User.get_full_name(objdev)
            proyecto = newTrabajo.userStory.proyecto
            id_proyecto = proyecto.id
            rolSM = Group.objects.filter(name = "Scrum Master")
            equipi = MiembroEquipo.objects.get(rol = rolSM, proyecto_id = id_proyecto)
            SM = equipi.usuario
            correo = SM.email
            send_mail("Asunto", "Mensaje del sistema. \nEl usuario " + str(desarrollador) + " ha creado el siguiente Trabajo\n" +
                      "\nDescrpcion: " + newTrabajo.descripcion +
                      "\nUser Story: " + newTrabajo.userStory.nombre +
                      "\nTipo de trabajo: " + str(newTrabajo.tipo_trabajo) +
                      "\nHoras: " + str(newTrabajo.hora) +
                      "\nFecha: " + str(newTrabajo.fecha),
                      '"SIGEPRO" <sigepro-is2@gmail.com>',[correo])

            #guardar archivo

                #guardar atributos
        return render_to_response('trabajos/creacion_correcta.html',{'id_userStory': id_userStory}, context_instance=RequestContext(request))
    else:

        formulario = crearTrabajoForm()
        hijo=False
        #proyecto=Proyecto.objects.filter(id=flujo.proyecto_id)
        return render_to_response('trabajos/crear_trabajos.html', { 'formulario': formulario}, context_instance=RequestContext(request))


def upload_listar(request, id_trabajo):
    trabajo = Trabajo.objects.get(id = id_trabajo)
    us = trabajo.userStory.id
    task = Trabajo.objects.filter(userStory_id = us)
    if request.method == 'POST':
        adjunto = Adjunto(nombre=request.POST['nombre'], descripcion=request.POST['descripcion'], binario=request.FILES['file'].read(),
                          content_type = request.FILES['file'].content_type, trabajo_id=id_trabajo)
        adjunto.save()
        return render_to_response('trabajos/listar_trabajos.html', {'datos':task, 'id_userStory': us},
                                  context_instance=RequestContext(request))
    else:
        hayAdjunto = Adjunto.objects.filter(trabajo_id = id_trabajo)
        userStory = UserStory.objects.get(id = trabajo.userStory_id)
        #flujo = Flujo.objects.get(id = userStory.flujo_id)
        proyecto = Proyecto.objects.get(id = userStory.proyecto_id)
        if hayAdjunto.count() == 0: # si no hay adjuntos.. muestra el template para cargar
            formulario = NuevoAdjunto()
            return render_to_response('trabajos/adjuntar.html',{'id_trabajo': id_trabajo, 'formulario': formulario, 'proyecto': proyecto},
                                      context_instance = RequestContext(request))
        else: # muestra el adjunto
            adjunto = Adjunto.objects.get(trabajo_id = id_trabajo)
            return render_to_response('trabajos/ver_adjunto.html',{'id_trabajo': id_trabajo, 'proyecto': proyecto, 'adjunto': adjunto},
                                      context_instance = RequestContext(request))



def upload_handler(request, attachment, uploaded_file,id_trabajo):
        #attachment.user_story = self.user_story
        attachment.nombre = uploaded_file.name


        attachment.content_type = uploaded_file.content_type
        attachment.binario = uploaded_file.read()
        attachment.save()
        return render_to_response('trabajos/adjuntar.html',{'id_trabajo': id_trabajo},context_instance = RequestContext(request))

# def form_valid(self, form):
#         attachment = form.save(commit=False)
#         self.upload_handler(attachment, self.request.FILES['file'])
#         return HttpResponseRedirect(attachment.get_absolute_url())




@login_required
def download_attachment(request, pk):
    """
    Vista que permite la descarga de un archivo adjunto de la base de datos
    :param request: request del cliente
    :param pk: id del adjunto
    :return: respuesta http con el archivo adjunto
    """
    attachment = get_object_or_404(Adjunto, pk=pk)
    #if request.user.has_perm('project.view_project', attachment.user_story.proyecto):
    response = HttpResponse(attachment.binario, content_type=attachment.content_type)
    response['Content-Disposition'] = 'attachment; nombre=%s' % attachment.nombre
    # if attachment.tipo == 'img':
    #     response['Content-Disposition'] = 'filename=%s' % attachment.filename
    # else:
    #     response['Content-Disposition'] = 'attachment; filename=%s' % attachment.filename
    return response
    #raise PermissionDenied()