# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0003_auto_20150515_0404'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='duracion_sprint',
        ),
    ]
