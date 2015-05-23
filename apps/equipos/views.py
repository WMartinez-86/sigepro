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
    SM = MiembroEquipo.objects.get(rol = rolSM, proyecto_id = id_proyecto)
    SMUser = User.objects.get(id = SM.usuario_id)

    dato = get_object_or_404(Proyecto, pk=id_proyecto)
    equipos = MiembroEquipo.objects.filter(proyecto_id = id_proyecto)
    #usuarios = User.objects.filter(id = equipos.usuario)

    # equipi = MiembroEquipo.objects.get(proyecto_id = id_proyecto)
    # comite = User.objects.filter(miembroequipo__id=id_proyecto) #filtra usuarios del comite
    #lider = get_object_or_404(User, pk=dato.lider_id)
    #flujos = Flujo.objects.filter(proyecto_id=id_proyecto)
    # nombre_roles = []
    usuarios = []
    #
    # roles = Group.objects.filter(proyecto_id=id_proyecto)
    # for rol in roles:
    #     nombre_roles.append(rol)
    #     u = User.objects.filter(groups__id=rol.id)
    #
    for nose in equipos:
        u = User.objects.filter(id = nose.usuario_id)
        #rol = Group.objects.filter(id = nose.rol_id)
        for user in u:
            uu = user.first_name + " " + user.last_name  + ", "  +"\n"
            usuarios.append(uu)


    return render_to_response('equipos/ver_equipo.html',
                          {'proyectos': dato, 'usuarios': usuarios, 'scrumMaster': SMUser},
                          context_instance=RequestContext(request))



