# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('criteria', models.CharField(verbose_name='criteria', max_length=250)),
                ('score', models.PositiveIntegerField(verbose_name='score')),
                ('object_id', models.PositiveIntegerField()),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='added at')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('score', models.PositiveIntegerField(verbose_name='score', max_length=250)),
                ('rating', models.ForeignKey(related_name='votes', to='rating.Rating', verbose_name='rating')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
