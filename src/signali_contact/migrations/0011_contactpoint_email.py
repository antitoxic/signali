# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0010_auto_20150908_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='contactpoint',
            name='email',
            field=models.EmailField(blank=True, verbose_name='Email', max_length=255),
        ),
    ]
