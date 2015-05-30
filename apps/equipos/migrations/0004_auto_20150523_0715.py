# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0003_auto_20150517_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miembroequipo',
            name='horasPorDia',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
