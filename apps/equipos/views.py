from django.shortcuts import render
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.models import User, Group, Permission
from apps.inicio.models import Perfiles
from apps.inicio.forms import UserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.


grupo, created = Group.objects.get_or_create(name='Equipo de trabajo')
if created:
    print 'grupo creado'
    grupo.save()


#obtenemos el id del permiso, el que es creado de forma automática cuando usamos syncdb
permiso = Permission.objects.get_by_natural_key(name='Can add escritor')
#agregamos el permiso
grupo.permissions.add(permiso)



def ingresar_usuario(request):
    user_form = UserFormStaff(request.POST or None)
    escritor_form = escritorForm(request.POST or None)

    if request.POST:
        user_form_valid = user_form.is_valid()
        escritor_form_valid = escritor_form.is_valid()
        if user_form_valid:
            if escritor_form_valid:
                new_user = User.objects.create_user(user_form.cleaned_data['username'], '', user_form.cleaned_data['password'])
                print new_user
                grupo = get_object_or_404(Group, name = 'Equipo de trabajo')
                if grupo != None:
                    new_user.groups.add(grupo)
                    new_user.is_active = True
                    new_user.is_staff = True
                    new_user.is_superuser = False
                    new_user.set_password(user_form.cleaned_data['password'])
                    new_user.save()
                    escritor = escritor_form.save(commit=False)
                    escritor.user = new_user
                    escritor.save()
                    return HttpResponseRedirect('/escritores/')
                else:
                    pass
    context = {
    'user_form' : user_form,
    'escritor_form' : escritor_form,
    }

    return render_to_response('ingresar_escritor.html', context, context_instance=RequestContext(request))