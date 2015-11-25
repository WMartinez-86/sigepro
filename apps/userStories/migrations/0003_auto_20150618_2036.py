# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userStories', '0002_userstory_tiempo_registrado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='tiempo_registrado',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Tiempo Registrado'),
        ),
    ]
