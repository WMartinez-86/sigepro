# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userStories', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userstory',
            name='tiempo_registrado',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Tiempo Registrado'),
            preserve_default=False,
        ),
    ]
