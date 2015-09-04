# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signali_contact', '0004_auto_20150903_0029'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpoint',
            name='notes',
            field=models.TextField(verbose_name='notes', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='proposed_by',
            field=models.ForeignKey(verbose_name='User that proposed it', blank=True, to=settings.AUTH_USER_MODEL, related_name='contactpoint_proposals', null=True),
            preserve_default=True,
        ),
    ]
