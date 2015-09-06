# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_location', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='views',
            field=models.PositiveIntegerField(verbose_name='views', default=0),
        ),
        migrations.AlterField(
            model_name='areasize',
            name='views',
            field=models.PositiveIntegerField(verbose_name='views', default=0),
        ),
    ]
