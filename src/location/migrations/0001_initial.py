# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('parent', models.ForeignKey(blank=True, related_name='children', verbose_name='parent area', null=True, to='location.Area')),
            ],
            options={
                'verbose_name': 'area',
                'verbose_name_plural': 'areas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AreaSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
            ],
            options={
                'verbose_name': 'area size',
                'verbose_name_plural': 'area sizes',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='area',
            name='size',
            field=models.ForeignKey(blank=True, related_name='areas', verbose_name='size', null=True, to='location.AreaSize'),
            preserve_default=True,
        ),
    ]
