# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0006_auto_20150903_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpoint',
            name='proposed_by',
            field=models.ForeignKey(verbose_name='user that proposed it', to=settings.AUTH_USER_MODEL, null=True, related_name='contactpoint_proposals', blank=True),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='address',
            field=models.OneToOneField(to='signali_location.Area', null=True, parent_link=True, on_delete=django.db.models.deletion.SET_NULL, blank=True),
        ),
        migrations.AlterField(
            model_name='signalcontactpointfeedback',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, related_name='feedback_given'),
        ),
    ]
