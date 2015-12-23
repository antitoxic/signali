# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0016_auto_20150910_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpoint',
            name='accessibility',
            field=models.IntegerField(verbose_name='Overall ease of access', default=0),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='effectiveness',
            field=models.IntegerField(verbose_name='Overall effectiveness', default=0),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='feedback_count',
            field=models.PositiveIntegerField(verbose_name='Overall feedback activity', default=0),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='parent',
            field=models.ForeignKey(to='signali_contact.ContactPoint', related_name='children', null=True),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='rating',
            field=models.FloatField(verbose_name='Overall rating', default=0),
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='operational_area',
            field=models.ForeignKey(verbose_name='operational area', to='signali_location.Area', related_name='contact_points', null=True),
        ),
    ]
