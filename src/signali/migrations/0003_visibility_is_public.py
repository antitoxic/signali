# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali', '0002_auto_20150730_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='visibility',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='is public'),
            preserve_default=True,
        ),
    ]
