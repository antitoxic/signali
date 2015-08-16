# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import signali.uploads
import sorl.thumbnail.fields
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('popularity', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('is_featured', models.BooleanField(default=False, verbose_name='is featured')),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
                ('style', models.CharField(verbose_name='Style [technical]', max_length=255, null=True, blank=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('slug', models.SlugField(verbose_name='URL part', max_length=255)),
                ('contents', redactor.fields.RedactorField(verbose_name='Content')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Added at')),
                ('changed_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Added at')),
                ('preview', sorl.thumbnail.fields.ImageField(upload_to=signali.uploads.Uploader('visibility'), verbose_name='preview', null=True, blank=True)),
                ('cover', sorl.thumbnail.fields.ImageField(upload_to=signali.uploads.Uploader('visibility'), verbose_name='cover', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'pages',
                'verbose_name': 'page',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
