# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('criteria', models.CharField(verbose_name='criteria', max_length=250)),
                ('score', models.PositiveIntegerField(verbose_name='score')),
                ('object_id', models.PositiveIntegerField()),
                ('added_at', models.DateTimeField(verbose_name='added at', default=django.utils.timezone.now)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('score', models.PositiveIntegerField(verbose_name='score', max_length=250)),
                ('rating', models.ForeignKey(verbose_name='rating', related_name='votes', to='rating.Rating')),
                ('user', models.ForeignKey(verbose_name='voter', related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
