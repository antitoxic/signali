# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import signali.uploads


class Migration(migrations.Migration):

    dependencies = [
        ('signali', '0002_setting_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('popularity', models.PositiveIntegerField(verbose_name='popularity', default=0)),
                ('views', models.PositiveIntegerField(verbose_name='views', default=0)),
                ('is_featured', models.BooleanField(verbose_name='is featured', default=False)),
                ('is_public', models.BooleanField(verbose_name='is public', default=False)),
                ('style', models.CharField(verbose_name='Style [technical]', max_length=255, blank=True, null=True)),
                ('order', models.PositiveIntegerField()),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('url', models.URLField(verbose_name='title', max_length=250)),
                ('provides', models.CharField(verbose_name='provides', max_length=250)),
                ('logo', sorl.thumbnail.fields.ImageField(upload_to=signali.uploads.Uploader('signali'), verbose_name='logo', blank=True, null=True)),
            ],
            options={
                'verbose_name': 'setting',
                'verbose_name_plural': 'settings',
            },
        ),
    ]
