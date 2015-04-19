# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpoint',
            name='slug',
            field=models.SlugField(verbose_name='slug', blank=True, max_length=255),
            preserve_default=True,
        ),
    ]
