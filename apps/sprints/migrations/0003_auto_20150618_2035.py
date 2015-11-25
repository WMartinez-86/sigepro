# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0002_auto_20150530_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='fin_propuesto',
            field=models.DateField(verbose_name=b'Fecha de Fin Propuesto, formato  DD/MM/AAAA'),
        ),
        migrations.AlterField(
            model_name='sprint',
            name='inicio_propuesto',
            field=models.DateField(verbose_name=b'Fecha de Inicio Propuesto, formato  DD/MM/AAAA'),
        ),
    ]
