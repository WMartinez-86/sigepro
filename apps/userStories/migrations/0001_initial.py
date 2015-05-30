# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('flujos', '0003_remove_flujo_finicio'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('proyectos', '0007_auto_20150528_1536'),
        ('actividades', '0001_initial'),
        ('sprints', '0003_auto_20150523_0715'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20, verbose_name=b'Nombre')),
                ('descripcion', models.TextField(verbose_name=b'Descripcion')),
                ('prioridad', models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])),
                ('valor_negocio', models.PositiveIntegerField(verbose_name=b'Valor de Negocio')),
                ('valor_tecnico', models.PositiveIntegerField(verbose_name=b'Valor Tecnico')),
                ('tiempo_estimado', models.PositiveIntegerField(verbose_name=b'Tiempo Estimado')),
                ('ultimo_cambio', models.DateTimeField(auto_now=True, verbose_name=b'Ultimo Cambio')),
                ('estadoKanban', models.IntegerField(default=0, choices=[(0, b'ToDo'), (1, b'Doing'), (2, b'Done'), (3, b'Pendiente Aprobacion'), (4, b'Aprobado')])),
                ('estadoScrum', models.IntegerField(default=0, choices=[(0, b'Nuevo'), (1, b'Iniciado'), (2, b'Suspendido'), (3, b'Eliminado')])),
                ('version', models.PositiveIntegerField(null=True, blank=True)),
                ('orden', models.PositiveIntegerField(null=True, blank=True)),
                ('fecha_mod', models.DateField(verbose_name=b'Fecha de Modificacion')),
                ('actividad', models.ForeignKey(blank=True, to='actividades.Actividad', null=True)),
                ('desarrollador', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('flujo', models.ForeignKey(blank=True, to='flujos.Flujo', null=True)),
                ('proyecto', models.ForeignKey(to='proyectos.Proyecto')),
                ('sprint', models.ForeignKey(to='sprints.Sprint')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VersionUserStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20, verbose_name=b'Nombre')),
                ('descripcion', models.TextField(verbose_name=b'Descripcion')),
                ('prioridad', models.IntegerField(default=1, choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)])),
                ('valor_negocio', models.PositiveIntegerField(verbose_name=b'Valor de Negocio')),
                ('valor_tecnico', models.PositiveIntegerField(verbose_name=b'Valor Tecnico')),
                ('tiempo_estimado', models.PositiveIntegerField(verbose_name=b'Tiempo Estimado')),
                ('ultimo_cambio', models.DateTimeField(auto_now=True, verbose_name=b'Ultimo Cambio')),
                ('estadoKanban', models.IntegerField(default=0, choices=[(0, b'ToDo'), (1, b'Doing'), (2, b'Done'), (3, b'Pendiente Aprobacion'), (4, b'Aprobado')])),
                ('estadoScrum', models.IntegerField(default=0, choices=[(0, b'Nuevo'), (1, b'Iniciado'), (2, b'Suspendido'), (3, b'Eliminado')])),
                ('version', models.PositiveIntegerField(null=True, blank=True)),
                ('orden', models.PositiveIntegerField(null=True, blank=True)),
                ('fecha_mod', models.DateField(verbose_name=b'Fecha de Modificacion')),
                ('actividad', models.ForeignKey(blank=True, to='actividades.Actividad', null=True)),
                ('flujo', models.ForeignKey(blank=True, to='flujos.Flujo', null=True)),
                ('id_UserStory', models.ForeignKey(related_name=b'userStoryVersion', verbose_name=b'UserStory', to='userStories.UserStory')),
                ('proyecto', models.ForeignKey(to='proyectos.Proyecto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
