# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0002_auto_20150515_0124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='estado',
            field=models.CharField(default=b'PRO', max_length=3, choices=[(b'PRO', b'Produccion'), (b'APR', b'Aprobado'), (b'FIN', b'Finalizado'), (b'ELI', b'Eliminado')]),
        ),
    ]
