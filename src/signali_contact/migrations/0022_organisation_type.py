# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0021_auto_20151223_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='organisation',
            name='type',
            field=models.CharField(max_length=20, choices=[('gov', 'Government'), ('ngo', 'NGO'), ('unofficial', 'Unofficial')], verbose_name='type', default='gov'),
        ),
    ]
