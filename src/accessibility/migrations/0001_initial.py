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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(max_length=255, verbose_name='URL part')),
                ('contents', redactor.fields.RedactorField(verbose_name='Content')),
                ('created_at', models.DateTimeField(verbose_name='Added at', default=django.utils.timezone.now)),
                ('changed_at', models.DateTimeField(verbose_name='Added at', default=django.utils.timezone.now)),
                ('is_public', models.BooleanField(verbose_name='Published', default=False)),
            ],
            options={
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
            bases=(models.Model,),
        ),
    ]
