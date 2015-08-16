# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('description', models.CharField(verbose_name='description', max_length=250)),
                ('google_analytics', models.CharField(verbose_name='google analytics account id', max_length=250)),
                ('areasize_address', models.ForeignKey(to='signali_location.AreaSize', verbose_name='Which size denotes address-level area')),
            ],
            options={
                'verbose_name_plural': 'settings',
                'verbose_name': 'setting',
            },
            bases=(models.Model,),
        ),
    ]
