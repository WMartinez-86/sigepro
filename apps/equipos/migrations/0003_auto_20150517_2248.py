# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0002_auto_20150515_0124'),
    ]

    operations = [
        migrations.RenameField(
            model_name='miembroequipo',
            old_name='roles',
            new_name='rol',
        ),
    ]
