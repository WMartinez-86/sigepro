# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='miembroequipo',
            old_name='fuerza_trabajo',
            new_name='horasPorDia',
        ),
    ]
