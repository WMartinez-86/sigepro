# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='fin_propuesto',
            field=models.DateField(null=True, verbose_name=b'Fecha de Inicio, formato  DD/MM/AAAA'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sprint',
            name='inicio_propuesto',
            field=models.DateField(null=True, verbose_name=b'Fecha de Inicio, formato  DD/MM/AAAA'),
            preserve_default=True,
        ),
    ]
