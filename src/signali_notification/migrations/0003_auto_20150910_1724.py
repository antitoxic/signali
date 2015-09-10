# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signali_notification', '0002_auto_20150905_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='user',
            field=models.ForeignKey(blank=True, null=True, related_name='subscriptions', verbose_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='subscriber',
            name='email',
            field=models.EmailField(null=True, verbose_name='email', max_length=250, blank=True),
        ),
    ]
