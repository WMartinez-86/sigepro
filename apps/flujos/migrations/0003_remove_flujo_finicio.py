# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flujos', '0002_flujo_proyecto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flujo',
            name='fInicio',
        ),
    ]
