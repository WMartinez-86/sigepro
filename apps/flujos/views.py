from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib import messages
from apps.proyectos.models import Proyecto
from apps.flujos.models import Flujo
from datetime import datetime
from apps.flujos.forms import FlujoForm, ModificarFlujoForm, CrearFlujoForm

# Create your views here.

@login_required
@permission_required('flujo')
def registrar_flujo(request, id_proyecto):
    """
    Vista para registrar una nueva fase dentro de proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return HttpResponseRedirect('/fases/register/success') si el rol lider fue correctamente asignado o
    render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request)) al formulario
    """
    mensaje=100
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if request.method=='POST':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        formulario = CrearFlujoForm(request.POST)
        # if formulario.is_valid():
        #     if len(str(request.POST["fInicio"])) != 10 : #Comprobacion de formato de fecha
        #         mensaje=0
        #         return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'mensaje':mensaje,'id':id_proyecto}, context_instance=RequestContext(request))
        #     else:
        #         fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%Y')
        #         fecha=fecha.strftime('%Y-%m-%d')
        #         fecha1=datetime.strptime(fecha,'%Y-%m-%d')
        #         newFase = Fase(nombre = request.POST["nombre"],descripcion = request.POST["descripcion"],maxItems = request.POST["maxItems"],
        #                        fInicio = fecha,estado = "PEN", proyecto_id = id_proyecto)
        #         aux=0
        #         orden=Fase.objects.filter(proyecto_id=id_proyecto)
        #
        #         if aux>0:
        #             aux=1
        #         else:
        #             proyecto=Proyecto.objects.get(id=id_proyecto)
        #             cantidad = orden.count()
        #             if cantidad>0:#comprobaciones de fecha
        #                anterior = Fase.objects.get(orden=cantidad, proyecto_id=id_proyecto)
        #                if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
        #                    #Fecha de inicio no concuerda con fase anterior
        #                    return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'mensaje':1,'id':id_proyecto,'proyecto':proyecto},
        #                                              context_instance=RequestContext(request))
        #                else:
        #                     if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
        #                         #Fecha de inicio no concuerda con proyecto
        #                         print(fecha1)
        #                         print(datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d'))
        #                         print (datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d'))
        #                         return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'mensaje':2,'id':id_proyecto,'proyecto':proyecto},
        #                                                   context_instance=RequestContext(request))
        #                     else:
        #                         newFase.orden=orden.count()+1 #Calculo del orden de la fase a crear
        #                         newFase.save()
        #                         return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
        #             else:
        #                 newFase.orden=1
        #                 newFase.save()
        #                 return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = CrearFlujoForm() #formulario inicial
    return render_to_response('flujos/registrar_flujos.html',{'formulario':formulario,'id':id_proyecto, 'proyecto':proyecto, 'mensaje':mensaje},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos, flujos')
def listar_flujos(request,id_proyecto):
    """
    vista para listar las fases del proyectos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('fases/listar_fases.html', {'datos': fases}, context_instance=RequestContext(request))
    """
    flujos = Flujo.objects.filter(proyecto_id=id_proyecto).order_by('orden')
    proyecto = Proyecto.objects.get(id=id_proyecto)
    # if proyecto.estado!='PEN':
    #     proyectos = Proyecto.objects.all().exclude(estado='ELI')
    #     return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos,'mensaje':1}, context_instance=RequestContext(request))
    # else:
    return render_to_response('flujos/listar_flujos.html', {'datos': flujos, 'proyecto' : proyecto}, context_instance=RequestContext(request))

