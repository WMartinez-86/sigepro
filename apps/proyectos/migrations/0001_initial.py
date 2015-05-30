# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(unique=True, max_length=50, verbose_name=b'Nombre')),
                ('nombreCorto', models.CharField(unique=True, max_length=20, verbose_name=b'Nombre')),
                ('siglas', models.CharField(max_length=20)),
                ('descripcion', models.TextField(verbose_name=b'Descripcion')),
                ('fecha_ini', models.DateField(verbose_name=b'Fecha de inicio')),
                ('fecha_fin', models.DateField(verbose_name=b'Fecha de Finalizacion')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(default=b'PEN', max_length=3, choices=[(b'PRO', b'Produccion'), (b'APR', b'Aprobado'), (b'FIN', b'Finalizado'), (b'ELI', b'Eliminado')])),
                ('duracion_sprint', models.PositiveIntegerField(default=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
