# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='views',
            field=models.PositiveIntegerField(verbose_name='views', default=0),
        ),
        migrations.AlterField(
            model_name='keyword',
            name='views',
            field=models.PositiveIntegerField(verbose_name='views', default=0),
        ),
    ]
