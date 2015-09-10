# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0015_signalcontactpointfeedback_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpoint',
            name='anonymous_visits',
            field=models.PositiveIntegerField(verbose_name='anonymous visits', default=0),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='last_visited_at',
            field=models.DateTimeField(null=True, verbose_name='created at', blank=True),
        ),
    ]
