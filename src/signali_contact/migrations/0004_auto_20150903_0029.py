# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0003_auto_20150902_1244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpoint',
            name='url',
            field=models.URLField(blank=True, verbose_name='URL', max_length=255),
            preserve_default=True,
        ),
    ]
