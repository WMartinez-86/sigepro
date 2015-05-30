# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=20)),
                ('descripcion', models.TextField(verbose_name=b'Descripcion')),
                ('inicio', models.DateField(null=True, verbose_name=b'Fecha de Inicio, formato  DD/MM/AAAA')),
                ('fin', models.DateField(null=True, verbose_name=b'Fecha de Inicio, formato  DD/MM/AAAA')),
                ('estado', models.IntegerField(default=0, verbose_name=b'Estado', choices=[(0, b'Futuros'), (1, b'En Ejecucion'), (2, b'Finalizado')])),
                ('orden', models.SmallIntegerField(verbose_name=b'Orden')),
                ('capacidad', models.IntegerField(default=0, verbose_name=b'Capacidad')),
                ('horasUS', models.IntegerField(default=0, verbose_name=b'Horas User Story')),
                ('proyecto', models.ForeignKey(to='proyectos.Proyecto')),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'sprint',
                'verbose_name_plural': 'sprints',
            },
            bases=(models.Model,),
        ),
    ]
