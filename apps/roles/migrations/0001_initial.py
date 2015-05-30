# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyectos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('crear_usuario', models.BooleanField(default=False, verbose_name=b'Crear Usuario')),
                ('modificar_usuario', models.BooleanField(default=False, verbose_name=b'Crear Usuario')),
                ('consultar_usuario', models.BooleanField(default=False, verbose_name=b'Consultar Usuario')),
                ('crear_rol', models.BooleanField(default=False, verbose_name=b'Crear Rol')),
                ('modificar_rol', models.BooleanField(default=False, verbose_name=b'Modificar Rol')),
                ('eliminar_rol', models.BooleanField(default=False, verbose_name=b'Eliminar Rol')),
                ('consultar_rol', models.BooleanField(default=False, verbose_name=b'Consultar Rol')),
                ('crear_userStory', models.BooleanField(default=False, verbose_name=b'Crear User Story')),
                ('modificar_userStory', models.BooleanField(default=False, verbose_name=b'Modificar User Story')),
                ('consultar_userStory', models.BooleanField(default=False, verbose_name=b'Consultar User Story')),
                ('cambiarEstado_userStory', models.BooleanField(default=False, verbose_name=b'Cambiar Estado User Story')),
                ('crear_proyecto', models.BooleanField(default=False, verbose_name=b'Crear Proyecto')),
                ('modificar_proyecto', models.BooleanField(default=False, verbose_name=b'Modificar Proyecto')),
                ('consultar_proyecto', models.BooleanField(default=False, verbose_name=b'Consultar Proyecto')),
                ('proyecto', models.ForeignKey(to='proyectos.Proyecto', null=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
