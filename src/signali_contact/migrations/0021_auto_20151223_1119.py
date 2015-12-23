# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0020_extract_children'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpoint',
            name='source_url',
            field=models.URLField(null=True, blank=True, verbose_name='Source URL', max_length=255),
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='title',
            field=models.CharField(blank=True, verbose_name='title', max_length=250),
        ),
    ]
