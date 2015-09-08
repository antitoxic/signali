# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0008_auto_20150906_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpoint',
            name='created_at',
            field=models.DateTimeField(verbose_name='Created at', default=django.utils.timezone.now),
        ),
    ]
