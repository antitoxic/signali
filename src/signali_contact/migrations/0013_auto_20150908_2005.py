# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0012_auto_20150908_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpoint',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='email',
            field=models.EmailField(blank=True, max_length=250, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='signalcontactpointfeedback',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, 'Weak'), (2, 'Could be better'), (3, 'Adequate'), (4, 'Good'), (5, 'Excellent')], default=0, verbose_name='Overall rating'),
        ),
    ]
