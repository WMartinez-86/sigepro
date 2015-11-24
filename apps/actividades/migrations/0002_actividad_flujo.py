# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0001_initial'),
        ('flujos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='actividad',
            name='flujo',
            field=models.ForeignKey(to='flujos.Flujo'),
            preserve_default=True,
        ),
    ]
