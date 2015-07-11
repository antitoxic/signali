# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
        ('contact', '0001_initial'),
        ('taxonomy', '0002_auto_20150711_1028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='Title', max_length=255)),
                ('slug', models.SlugField(verbose_name='URL part', max_length=255)),
                ('contents', redactor.fields.RedactorField(verbose_name='Content')),
                ('created_at', models.DateTimeField(verbose_name='Added at', default=django.utils.timezone.now)),
                ('changed_at', models.DateTimeField(verbose_name='Added at', default=django.utils.timezone.now)),
                ('is_public', models.BooleanField(verbose_name='Published', default=False)),
                ('style', models.CharField(null=True, verbose_name='Style [technical]', max_length=255, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('description', models.CharField(verbose_name='description', max_length=250)),
                ('google_analytics', models.CharField(verbose_name='google analytics account id', max_length=250)),
                ('areasize_address', models.ForeignKey(verbose_name='Which size denotes address-level area', to='location.AreaSize')),
            ],
            options={
                'verbose_name': 'settting',
                'verbose_name_plural': 'setttings',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Visibility',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('popularity', models.PositiveIntegerField(verbose_name='popularity', default=0)),
                ('views', models.PositiveIntegerField(verbose_name='popularity', default=0)),
                ('is_featured', models.BooleanField(verbose_name='is featured', default=False)),
                ('category', models.OneToOneField(verbose_name='category', blank=True, null=True, related_name='visibility', to='taxonomy.Category')),
                ('contactpoint', models.OneToOneField(verbose_name='contact point', blank=True, null=True, related_name='visibility', to='contact.ContactPoint')),
                ('organisation', models.OneToOneField(verbose_name='organisation', blank=True, null=True, related_name='visibility', to='contact.Organisation')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
