# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('parent', models.ForeignKey(related_name='children', to='taxonomy.Category', null=True, verbose_name='parent category', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('style', models.CharField(verbose_name='style', max_length=250)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
