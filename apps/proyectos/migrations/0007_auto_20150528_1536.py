# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0006_auto_20150526_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='fecha_apr',
            field=models.DateField(null=True, verbose_name=b'Fecha de Aprobacion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='proyecto',
            name='fecha_eli',
            field=models.DateField(null=True, verbose_name=b'Fecha de Eliminacion'),
            preserve_default=True,
        ),
    ]
