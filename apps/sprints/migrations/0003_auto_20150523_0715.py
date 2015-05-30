# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0002_auto_20150502_0841'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='estado',
            field=models.IntegerField(default=0, verbose_name=b'Estado', choices=[(0, b'BackLog'), (1, b'En Ejecucion'), (2, b'Finalizado')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sprint',
            name='fin',
            field=models.DateField(null=True, verbose_name=b'Fecha de Inicio, formato  DD/MM/AAAA'),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='inicio',
            field=models.DateField(null=True, verbose_name=b'Fecha de Inicio, formato  DD/MM/AAAA'),
        ),
    ]
