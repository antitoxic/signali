# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import signali.uploads
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('popularity', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('is_featured', models.BooleanField(default=False, verbose_name='is featured')),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
                ('style', models.CharField(verbose_name='Style [technical]', blank=True, null=True, max_length=255)),
                ('preview', sorl.thumbnail.fields.ImageField(verbose_name='preview', upload_to=signali.uploads.Uploader('visibility'), blank=True, null=True)),
                ('cover', sorl.thumbnail.fields.ImageField(verbose_name='cover', upload_to=signali.uploads.Uploader('visibility'), blank=True, null=True)),
                ('parent', models.ForeignKey(to='signali_taxonomy.Category', null=True, verbose_name='parent category', related_name='children', blank=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('popularity', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('is_featured', models.BooleanField(default=False, verbose_name='is featured')),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
                ('style', models.CharField(verbose_name='Style [technical]', blank=True, null=True, max_length=255)),
                ('preview', sorl.thumbnail.fields.ImageField(verbose_name='preview', upload_to=signali.uploads.Uploader('visibility'), blank=True, null=True)),
                ('cover', sorl.thumbnail.fields.ImageField(verbose_name='cover', upload_to=signali.uploads.Uploader('visibility'), blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'keywords',
                'verbose_name': 'keyword',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
