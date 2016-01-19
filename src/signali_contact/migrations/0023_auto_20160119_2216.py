# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0022_organisation_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='type',
            field=models.CharField(default='gov', choices=[('gov', 'Government'), ('ngo', 'NGO'), ('unofficial', 'Unofficial'), ('commercial', 'Commercial')], max_length=20, verbose_name='type'),
        ),
    ]
