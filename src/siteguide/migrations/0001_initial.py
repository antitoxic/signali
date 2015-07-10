# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('slug', models.SlugField(verbose_name='URL part', max_length=255)),
                ('contents', redactor.fields.RedactorField(verbose_name='Content')),
                ('created_at', models.DateTimeField(verbose_name='Added at', default=django.utils.timezone.now)),
                ('changed_at', models.DateTimeField(verbose_name='Added at', default=django.utils.timezone.now)),
                ('is_public', models.BooleanField(verbose_name='Published', default=False)),
                ('style', models.CharField(verbose_name='Style [technical]', blank=True, max_length=255, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('description', models.CharField(verbose_name='description', max_length=250)),
                ('google_analytics', models.CharField(verbose_name='description', max_length=250)),
            ],
            options={
                'verbose_name': 'settting',
                'verbose_name_plural': 'setttings',
            },
            bases=(models.Model,),
        ),
    ]
