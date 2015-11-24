# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miembroequipo',
            name='horasPorDia',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Horas por dia'),
        ),
    ]
