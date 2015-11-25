# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trabajos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trabajo',
            name='hora',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Horas'),
        ),
    ]
