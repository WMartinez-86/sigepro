# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipos', '0004_auto_20150523_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='miembroequipo',
            name='proyecto',
            field=models.ForeignKey(to='proyectos.Proyecto', null=True),
        ),
    ]
