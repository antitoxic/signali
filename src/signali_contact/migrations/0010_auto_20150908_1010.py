# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0009_contactpoint_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpoint',
            name='is_other_required',
            field=models.BooleanField(verbose_name='required other', default=False),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='is_phone_required',
            field=models.BooleanField(verbose_name='required phone', default=False),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='other_requirements',
            field=models.TextField(blank=True, verbose_name='other requirements'),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='response_time',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Response time'),
        ),
    ]
