# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0007_auto_20150905_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpoint',
            name='views',
            field=models.PositiveIntegerField(verbose_name='views', default=0),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='views',
            field=models.PositiveIntegerField(verbose_name='views', default=0),
        ),
        migrations.AlterField(
            model_name='signalcontactpointfeedback',
            name='rating',
            field=models.PositiveIntegerField(verbose_name='Overall rating', null=True, choices=[(1, 'Weak'), (2, 'Could be better'), (3, 'Adequate'), (4, 'Good'), (5, 'Excellent')]),
        ),
    ]
