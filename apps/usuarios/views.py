# coding=utf-8
from django.views.generic import FormView, TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import resolve_url, render, redirect, get_object_or_404
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.forms import ModelForm
from django.contrib.auth.models import User
from apps.inicio.models import Perfiles
from apps.inicio.forms import UserForm
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views import generic


class Usuario(ModelForm):
    """
    Clase que representa el modelo de Usuario de Django
    @typ ModelForm:
    """
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

# class Perfil(ModelForm):
#     """
#     Modelo que agrega el rol de Scrum Master
#     """
#     class Meta:
#         model = Perfiles
#         fields = ('telefono', 'direccion')

@login_required
def list_usuario(request, template_name = 'usuarios/admin.html'):
    """
    Vista para la lista de usuarios
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param template_name: Nombre del template usado para la capa de presentación y listar los usuarios
    @return: render(request, template_name,data)
    """
    usuario = User.objects.all()
    data ={}
    data['object_list']= usuario
    return render(request, template_name,data)

@login_required
def delete_user(request, pk, template_name = 'usuarios/user/delete_user.html'):
    """
    Se eliminan usuarios
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param pk: referencia a la clave primaria del usuario
    @param template_name: El nombre completo del template usado para desplegar la interfaz de cambio de contraseña
    @return: render(request, template_name, usuario)
    """
    usuario = get_object_or_404(User, pk=pk)
    if request.method=='POST':
        usuario.delete()
        return redirect('usuario')
    return render(request, template_name, {'object':usuario})


@login_required
def edit_user(request, pk, template_name = 'usuarios/user/edit.html'):
    """
    Se modifican los Datos del Usuario
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param pk: referencia a la clave primaria del usuario
    @param template_name: El nombre completo del template usado para desplegar el formulario de edición de datos de usuario
    @return: render(request, template_name, {form, perfil} )
    """
    usuario = get_object_or_404(User, pk=pk)
    user= get_object_or_404(Perfiles, usuario=usuario)
    print(get_object_or_404(Perfiles, usuario=usuario))
    form = Usuario(request.POST or False, instance= usuario)
    #perfil = Perfil(request.POST or False, instance=user)
    # if form.is_valid() and perfil.is_valid():
    #     form.save()
    #     perfil.save()
        #return redirect('/usuarios/')
    return render(request, template_name, {'form':form})



@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='usuarios/user/cambiar_pass.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    """
    Verifica que no halla ningun error al cambiar el password
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param template_name: El nombre completo del template usado para desplegar el formulario de cambio de contraseña
    @param post_change_redirect: La URL a redirigir luego de un cambio exitoso de usuario
    @param password_change_form: Un formulario clásico de cambio de contraseña
    @param current_app: nombre de la aplicación que contiene a la vista actual
    @return: TemplateResponse(request, template_name, context, current_app=current_app)
    """
    if post_change_redirect is None:
        post_change_redirect = reverse('cambiar_pass_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

@login_required
def password_change_done(request,
                         template_name='usuarios/user/cambiar_pass_done.html',
                         current_app=None, extra_context=None):
    """
    Redirecciona a la siguiente pagina confirmando el cambio exitoso de password
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param template_name: El nombre completo del template usado para desplegar en la capa de presentación
    @param current_app: nombre de la aplicación que contiene a la vista actual
    @param extra_context: Un diccionario que contiene los datos del contexto que se agregan a los datos que ya se tienen
    @return: TemplateResponse(request, template_name, context, current_app=current_app)
    """
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


@login_required
def search(request):
    """
    Función de búsqueda de usuarios
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render(request, 'usuarios/admin.html',
            {'usuarios': usuarios, 'query': busqueda}) o redirige a /usuario/ si no encuentra la expresión regular
    """
    if 'busqueda' in request.GET and request.GET['busqueda']:
        busqueda = request.GET['busqueda']
        usuarios = User.objects.filter(username__contains=busqueda)
        return render(request, 'usuarios/admin.html',
            {'usuarios': usuarios, 'query': busqueda})
    else:
        return redirect('/usuario/')

# class Registrarse(FormView):
#     """
#     Recibe un @ctype  {FormView} y asigna un template para la operacion
#     @c param FormView
#     """
#     template_name = 'inicio/registrarse.html'
#     form_class = UserForm
#     success_url = reverse_lazy('registrarse')
#
#     def form_valid(self, form):
#         """
#         Formulario que valida los datos de usuario y perfil. Luego limpia los datos para comprobacion
#         @param self: referencia al objeto
#         @param form: Formulario de validacion del usuario
#         """
#         user = form.save()
#         perfil = Perfiles()
#         perfil.usuario = user
#         user.first_name = form.cleaned_data['first_name']
#         user.last_name = form.cleaned_data['last_name']
#         user.email = form.cleaned_data['email']
#         perfil.telefono = form.cleaned_data['telefono']
#         perfil.direccion = form.cleaned_data['direccion']
#         perfil.lider = False
#         user.is_active = False
#         user.is_staff = False
#         user.save()
#         perfil.save()
#         return super(Registrarse,self).form_valid(form)


class Registrarse(generic.CreateView):
    """
    Recibe un @ctype  {FormView} y asigna un template para la operacion
    @c param FormView
    """
    model = User
    template_name = 'usuarios/registrarse.html'
    form_class = UserForm
    success_url = reverse_lazy('registrarse')

    def get_success_url(self):
        """
        Retorna una los usuarios excluyendo el AnonymousUser

        :return: url del UserDetail
        """
        #return reverse('usuarios/user/admin.html', kwargs={'pk': self.object.id})
        return reverse_lazy('usuario')

    def form_valid(self, form):
        """
        Formulario que valida los datos de usuario y perfil. Luego limpia los datos para comprobacion
        @param self: referencia al objeto
        @param form: Formulario de validacion del usuario
        """
        # user = form.save()
        # perfil = Perfiles()
        # perfil.usuario = user
        # user.name = form.cleaned_data['name']
        # user.password = form.cleaned_data['password']
        # user.first_name = form.cleaned_data['first_name']
        # user.last_name = form.cleaned_data['last_name']
        # user.email = form.cleaned_data['email']
        # perfil.telefono = form.cleaned_data['telefono']
        # perfil.direccion = form.cleaned_data['direccion']
        # perfil.lider = False
        # user.is_active = False
        # user.is_staff = False
        # user.save()
        # perfil.save()
        super(Registrarse, self).form_valid(form)

        return HttpResponseRedirect(self.get_success_url())



# class AddUser(FormView):
#     """
#     Agregar un Usuario al Sistema
#     """
#     model = User
#     form_class = UserCreateForm
#     template_name = 'usuarios/registrarse.html'
#     permission_required = 'auth.add_user'
#
#     def get_success_url(self):
#         """
#         Retorna una los usuarios excluyendo el AnonymousUser
#
#         :return: url del UserDetail
#         """
#         return reverse('usuarios/user/admin.html', kwargs={'pk': self.object.id})
#
#     def form_valid(self, form):
#         """
#         Verificar validez del formulario
#
#         :param form: formulario completado
#         :return: Url de Evento Correcto
#         """
#         super(AddUser, self).form_valid(form)
#
#         escogidas = self.request.POST.getlist('general_perms')
#         #for permname in escogidas:
#             #perm = Permission.objects.get(codename=permname)
#             #self.object.user_permissions.add(perm)
#
#         return HttpResponseRedirect(self.get_success_url())
