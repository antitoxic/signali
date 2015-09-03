# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0002_auto_20150822_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpoint',
            name='url',
            field=models.URLField(verbose_name='url', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='signalcontactpointfeedback',
            name='user',
            field=models.ForeignKey(related_name='feedback_given', verbose_name='User', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
