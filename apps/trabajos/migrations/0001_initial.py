# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userStories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjunto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100, null=True)),
                ('descripcion', models.TextField()),
                ('binario', models.BinaryField(null=True, blank=True)),
                ('content_type', models.CharField(max_length=50, null=True, editable=False)),
                ('fechaCreacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trabajo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.TextField(max_length=140)),
                ('tipo_trabajo', models.SmallIntegerField(default=0, choices=[(0, b'Normal'), (1, b'Cambio de estado')])),
                ('hora', models.PositiveIntegerField(default=0)),
                ('fecha', models.DateField(verbose_name=b'Fecha')),
                ('userStory', models.ForeignKey(to='userStories.UserStory')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='adjunto',
            name='trabajo',
            field=models.ForeignKey(to='trabajos.Trabajo'),
            preserve_default=True,
        ),
    ]
