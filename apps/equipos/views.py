from django.shortcuts import render
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from apps.inicio.models import Perfiles
from apps.inicio.forms import UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from apps.proyectos.models import Proyecto
from apps.flujos.models import Flujo
from apps.equipos.models import MiembroEquipo
from apps.equipos.forms import crearEquipoForm

# Create your views here.

@login_required
@permission_required('proyectos')
def ver_equipo(request, id_proyecto):
    """
    vista para ver todos los usuarios que forman parte de un proyectos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/ver_equipo.html', {'proyectos':dato,'lider': lider, 'comite':comite, 'usuarios':usuarios}, context_instance=RequestContext(request))
    """
    rolSM = Group.objects.filter(name = "Scrum Master")
    haySM = MiembroEquipo.objects.filter(rol = rolSM, proyecto_id = id_proyecto)
    if haySM.count() > 0: #si hay Scrum Master
        SM = MiembroEquipo.objects.get(rol = rolSM, proyecto_id = id_proyecto)
        SMUser = User.objects.get(id = SM.usuario_id)
    else:
        SMUser = None
    proyecto = get_object_or_404(Proyecto, pk=id_proyecto)
    equipos = MiembroEquipo.objects.filter(proyecto_id = id_proyecto)


    return render_to_response('equipos/ver_equipo.html',
                          {'proyecto': proyecto, 'equipos': equipos, 'scrumMaster': SMUser},
                          context_instance=RequestContext(request))



@login_required
@permission_required('proyectos')
def agregar_miembro(request, id_proyecto):

     if request.method=='POST':
        #formset = ItemFormSet(request.POST)
        formulario = crearEquipoForm(request.POST)

        if formulario.is_valid():
            #newEquipo=MiembroEquipo(usuario_id = request.POST['usuario'], proyecto_id= id_proyecto, rol_id = request.POST['id_rol'],
            #                        horasPorDia=request.POST['horasPorDia'])
            #newEquipo.save()
            formulario.save()
        return render_to_response('equipos/creacion_correcta.html',{'id_proyecto': id_proyecto}, context_instance=RequestContext(request))
     else:
        formulario = crearEquipoForm(initial={'proyecto': id_proyecto})
        #hijo=False
        #proyecto=Proyecto.objects.filter(id=flujo.proyecto_id)
        return render_to_response('equipos/agregar_miembro.html', { 'formulario': formulario, 'id_proyecto': id_proyecto},
                                  context_instance=RequestContext(request))
