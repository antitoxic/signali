# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('location', '0001_initial'),
        ('accessibility', '0001_initial'),
        ('taxonomy', '0002_auto_20150711_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('description', models.CharField(verbose_name='description', max_length=250)),
                ('google_analytics', models.CharField(verbose_name='google analytics account id', max_length=250)),
                ('areasize_address', models.ForeignKey(verbose_name='Which size denotes address-level area', to='location.AreaSize')),
            ],
            options={
                'verbose_name_plural': 'settings',
                'verbose_name': 'setting',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visibility',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('popularity', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('views', models.PositiveIntegerField(default=0, verbose_name='popularity')),
                ('is_featured', models.BooleanField(default=False, verbose_name='is featured')),
                ('style', models.CharField(blank=True, verbose_name='Style [technical]', max_length=255, null=True)),
                ('category', models.OneToOneField(verbose_name='category', to='taxonomy.Category', related_name='visibility', blank=True, null=True)),
                ('contactpoint', models.OneToOneField(verbose_name='contact point', to='contact.ContactPoint', related_name='visibility', blank=True, null=True)),
                ('page', models.OneToOneField(verbose_name='page', to='accessibility.Page', related_name='visibility', blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'visibility records',
                'abstract': False,
                'verbose_name': 'visibility',
            },
            bases=(models.Model,),
        ),
    ]
