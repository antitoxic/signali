# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_location', '0004_auto_20151209_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='areasize',
            name='abbr',
            field=models.CharField(verbose_name='abbreviation', blank=True, max_length=250),
        ),
    ]
