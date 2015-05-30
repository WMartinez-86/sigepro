# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Flujo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, verbose_name=b'Nombre')),
                ('descripcion', models.TextField(verbose_name=b'Descripcion')),
                ('fInicio', models.DateField(verbose_name=b'Fecha de Inicio, formato  DD/MM/AAAA')),
                ('orden', models.SmallIntegerField(verbose_name=b'Orden')),
                ('estado', models.CharField(max_length=3, verbose_name=b'Estado', choices=[(b'PEN', b'Pendiente'), (b'EJE', b'En Ejecucion'), (b'FIN', b'Finalizado')])),
                ('fCreacion', models.DateField(auto_now=True, verbose_name=b'Fecha de Creacion')),
                ('roles', models.ManyToManyField(to='auth.Group')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
