import os


def populate():
    cli = agregar_rol('Cliente')
    adm = agregar_rol('Administrador')
    des = agregar_rol('Desarrollador')
    sm = agregar_rol('Scrum Master')

    u = agregar_usuario('manuel')
    c = agregar_usuario('juan')
    s = agregar_superUsuario('sergio')
    p = agregar_proyecto('PoblarBD', 'Poblar la Base de Datos')
    #agregar_miembrosEquipo(u, p, adm)
    #agregar_miembrosEquipo(c, p, cli)
    #agregar_miembrosEquipo(s, p, sm)

    print "terminado"


# TODO anhadir permisos
def agregar_rol(nombre, permisos=None):
    try:
        r = Group.objects.get(name=nombre)
    except Group.DoesNotExist:
        r = Group.objects.create(name=nombre)
        r.permissions.add(1)
    return r


def agregar_usuario(user, password='sigepro'):
    try:
        u = User.objects.get(username=user)
    except User.DoesNotExist:
        u = User.objects.create_user(user, "{}@gmail.com".format(user.lower()), password)
    return u


def agregar_superUsuario(user, password='sigepro'):
    try:
        u = User.objects.get(username=user)
    except User.DoesNotExist:
        u = User.objects.create_superuser(user, "{}@gmail.com".format(user.lower()), password)
        u.is_staff = True
        u.save()
    return u


def agregar_proyecto(nombreCorto, nombre, sprint=30):
    try:
        p = Proyecto.objects.get(nombreCorto=nombreCorto)
    except Proyecto.DoesNotExist:
        p = Proyecto.objects.get_or_create(nombreCorto=nombreCorto, nombre=nombre, duracion_sprint=sprint,
                                           fecha_ini=timezone.now(), fecha_fin=timezone.now())
    return p


# def agregar_miembrosEquipo(user, project, role):
#     try:
#         t = MiembroEquipo.objects.get(usuario=user.id, proyecto=project.id, rol=role.id)
#     except MiembroEquipo.DoesNotExist:
#         t = MiembroEquipo.objects.create(usuario=user, proyecto=project, rol=role)
#     return t

# Start execution here!
if __name__ == '__main__':
    print "Inicio de la poblacion de la base de datos"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigepro.settings')
    import django

    django.setup()
    from apps.proyectos.models import Proyecto#, MiembroEquipo
    from django.contrib.auth.models import User, Group
    from django.utils import timezone

    populate()
