# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('criteria', models.CharField(max_length=250, verbose_name='criteria')),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='added at')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('score', models.PositiveIntegerField(max_length=250, verbose_name='score')),
                ('added_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='added at')),
                ('rating', models.ForeignKey(verbose_name='rating', to='feedback.Rating', related_name='votes')),
                ('user', models.ForeignKey(verbose_name='voter', to=settings.AUTH_USER_MODEL, related_name='votes')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
