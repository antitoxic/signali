# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_accessibility', '0002_auto_20150905_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='views',
            field=models.PositiveIntegerField(verbose_name='views', default=0),
        ),
    ]
