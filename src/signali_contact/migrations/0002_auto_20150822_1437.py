# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='signalcontactpointfeedback',
            name='response_speed',
        ),
        migrations.RemoveField(
            model_name='signalcontactpointfeedback',
            name='usability',
        ),
        migrations.AddField(
            model_name='signalcontactpointfeedback',
            name='is_easy',
            field=models.BooleanField(default=False, verbose_name='Was it easy to operate with the contact point?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='signalcontactpointfeedback',
            name='is_effective',
            field=models.BooleanField(default=False, verbose_name='Are you happy with the results of your contact?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='signalcontactpointfeedback',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, 'Weak'), (2, 'Could be better'), (3, 'Adequate'), (4, 'Good'), (5, 'Excellent')], null=True, verbose_name='Overall rating', max_length=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='signalcontactpointfeedback',
            name='added_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Added at'),
            preserve_default=True,
        ),
    ]
