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
            name='Area',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('popularity', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('is_featured', models.BooleanField(default=False, verbose_name='is featured')),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
                ('style', models.CharField(max_length=255, null=True, verbose_name='Style [technical]', blank=True)),
                ('preview', sorl.thumbnail.fields.ImageField(upload_to=signali.uploads.Uploader('visibility'), null=True, verbose_name='preview', blank=True)),
                ('cover', sorl.thumbnail.fields.ImageField(upload_to=signali.uploads.Uploader('visibility'), null=True, verbose_name='cover', blank=True)),
                ('parent', models.ForeignKey(null=True, verbose_name='parent area', related_name='children', to='signali_location.Area', blank=True)),
            ],
            options={
                'verbose_name_plural': 'areas',
                'abstract': False,
                'verbose_name': 'area',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AreaSize',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('popularity', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('is_featured', models.BooleanField(default=False, verbose_name='is featured')),
                ('is_public', models.BooleanField(default=False, verbose_name='is public')),
                ('style', models.CharField(max_length=255, null=True, verbose_name='Style [technical]', blank=True)),
                ('preview', sorl.thumbnail.fields.ImageField(upload_to=signali.uploads.Uploader('visibility'), null=True, verbose_name='preview', blank=True)),
                ('cover', sorl.thumbnail.fields.ImageField(upload_to=signali.uploads.Uploader('visibility'), null=True, verbose_name='cover', blank=True)),
            ],
            options={
                'verbose_name_plural': 'area sizes',
                'abstract': False,
                'verbose_name': 'area size',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='area',
            name='size',
            field=models.ForeignKey(null=True, verbose_name='size', related_name='areas', to='signali_location.AreaSize', blank=True),
            preserve_default=True,
        ),
    ]
