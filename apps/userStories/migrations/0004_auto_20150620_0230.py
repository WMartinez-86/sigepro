# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userStories', '0003_auto_20150618_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='tiempo_estimado',
            field=models.PositiveIntegerField(verbose_name=b'Tiempo Estimado en Horas'),
        ),
    ]
