# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0004_remove_proyecto_duracion_sprint'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(default=b'PRO', max_length=3, choices=[(b'NUE', b'Nuevo'), (b'PRO', b'Produccion'), (b'FIN', b'Finalizado'), (b'APR', b'Aprobado'), (b'ELI', b'Eliminado')]),
        ),
    ]
