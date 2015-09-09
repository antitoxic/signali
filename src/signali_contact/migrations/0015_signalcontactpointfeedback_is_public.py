# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0014_contactpoint_visits'),
    ]

    operations = [
        migrations.AddField(
            model_name='signalcontactpointfeedback',
            name='is_public',
            field=models.BooleanField(verbose_name='is public', default=False),
        ),
    ]
