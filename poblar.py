import os

def populate():
    cli = agregar_rol('Cliente')
    adm = agregar_rol('Administrador')
    des = agregar_rol('Desarrollador')
    sm = agregar_rol('Scrum Master')

    m = agregar_usuario('manuel')
    e = agregar_usuario('ema')
    d = agregar_usuario('david')
    w = agregar_usuario('willian')
    o = agregar_usuario('otto')
    j = agregar_usuario('juan')
    s = agregar_superUsuario('sergio')
    pb = agregar_proyecto('PoblarBD', 'Poblar la Base de Datos')
    pp = agregar_proyecto('Pintar', 'Pintar la casa')
    pa = agregar_proyecto('ArmComp', 'Armar Computadora')
    agregar_miembrosEquipo(m, pb, adm)
    # agregar_miembrosEquipo(w, pb, cli)
    # agregar_miembrosEquipo(e, pb, sm)
    # agregar_miembrosEquipo(d, pb, des)
    # agregar_miembrosEquipo(d, pp, adm)
    # agregar_miembrosEquipo(o, pp, cli)
    # agregar_miembrosEquipo(s, pp, sm)
    # agregar_miembrosEquipo(m, pp, des)
    # agregar_miembrosEquipo(j, pp, des)
    # agregar_miembrosEquipo(m, pa, adm)
    # agregar_miembrosEquipo(j, pa, cli)
    # agregar_miembrosEquipo(s, pa, sm)
    # agregar_miembrosEquipo(d, pa, des)
    # agregar_miembrosEquipo(o, pa, des)
    # agregar_miembrosEquipo(w, pa, des)

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
        p = Proyecto.objects.get_or_create(nombreCorto=nombreCorto, nombre=nombre,
                                           fecha_ini=timezone.now(), fecha_fin=timezone.now() + timedelta(days=30))
    return p


def agregar_miembrosEquipo(user, project, role):
    try:
        t = MiembroEquipo.objects.get(usuario=user.id, proyecto=project.id, rol=role.id, horasPorDia=10)
    except MiembroEquipo.DoesNotExist:
        t = MiembroEquipo.objects.create(usuario=user, proyecto=project, rol_id=role, horasPorDia=10)
    return t

# def agregar_miembrosEquipo(user, project, role):
#     try:
#         t = MiembroEquipo.objects.get(usuario=user.id, proyecto=project.id, rol=role.id, horasPorDia=10)
#     except MiembroEquipo.DoesNotExist:
#         t = MiembroEquipo.objects.create(usuario=user, proyecto=project, rol=role, horasPorDia=10)
#     return t

# Start execution here!
if __name__ == '__main__':
    print "Inicio de la poblacion de la base de datos"
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigepro.settings')
    import django

    django.setup()
    from apps.proyectos.models import Proyecto
    from django.contrib.auth.models import User, Group
    from django.utils import timezone
    from datetime import timedelta
    from apps.equipos.models import MiembroEquipo

    populate()
