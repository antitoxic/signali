# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_location', '0003_auto_20150908_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='regulation_code',
            field=models.CharField(null=True, verbose_name='regulation code', max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='area',
            name='regulation_codename',
            field=models.CharField(null=True, verbose_name='regulation codename', max_length=20, blank=True),
        ),
        migrations.AddField(
            model_name='area',
            name='regulation_type',
            field=models.CharField(null=True, verbose_name='regulation type', max_length=20, blank=True),
        ),
    ]
