# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0013_auto_20150908_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpoint',
            name='visits',
            field=models.PositiveIntegerField(verbose_name='visits', default=0),
        ),
    ]
