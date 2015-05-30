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
                ('nombreCorto', models.CharField(unique=True, max_length=20, verbose_name=b'Nombre corto')),
                ('descripcion', models.TextField(verbose_name=b'Descripcion')),
                ('fecha_ini', models.DateField(null=True, verbose_name=b'Fecha de inicio')),
                ('fecha_fin', models.DateField(null=True, verbose_name=b'Fecha de Finalizacion')),
                ('fecha_apr', models.DateField(null=True, verbose_name=b'Fecha de Aprobacion')),
                ('fecha_eli', models.DateField(null=True, verbose_name=b'Fecha de Eliminacion')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('estado', models.CharField(default=b'NUE', max_length=3, choices=[(b'NUE', b'Nuevo'), (b'PRO', b'Produccion'), (b'FIN', b'Finalizado'), (b'APR', b'Aprobado'), (b'ELI', b'Eliminado')])),
            ],
            options={
                'default_permissions': (),
                'verbose_name': 'proyecto',
                'verbose_name_plural': 'proyectos',
            },
            bases=(models.Model,),
        ),
    ]
