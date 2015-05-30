# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0001_initial'),
        ('flujos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='flujo',
            name='proyecto',
            field=models.ForeignKey(default=1, to='proyectos.Proyecto'),
            preserve_default=False,
        ),
    ]
