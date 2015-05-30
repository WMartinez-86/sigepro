# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0005_auto_20150525_2347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='siglas',
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(default=b'NUE', max_length=3, choices=[(b'NUE', b'Nuevo'), (b'PRO', b'Produccion'), (b'FIN', b'Finalizado'), (b'APR', b'Aprobado'), (b'ELI', b'Eliminado')]),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fecha_fin',
            field=models.DateField(null=True, verbose_name=b'Fecha de Finalizacion'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fecha_ini',
            field=models.DateField(null=True, verbose_name=b'Fecha de inicio'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='nombreCorto',
            field=models.CharField(unique=True, max_length=20, verbose_name=b'Nombre corto'),
        ),
    ]
