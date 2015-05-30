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
            name='descripcion',
            field=models.TextField(default='desc', verbose_name=b'Descripcion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sprint',
            name='orden',
            field=models.SmallIntegerField(default=1, verbose_name=b'Orden'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sprint',
            name='fin',
            field=models.DateField(verbose_name=b'Fecha de Inicio, formato  DD/MM/AAAA'),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='inicio',
            field=models.DateField(verbose_name=b'Fecha de Inicio, formato  DD/MM/AAAA'),
        ),
    ]
