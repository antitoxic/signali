# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0018_contactpointgrouped'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactpointgrouped',
            options={'verbose_name_plural': 'Contact point groups', 'verbose_name': 'Grouped contact point'},
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='source_url',
            field=models.URLField(verbose_name='URL', blank=True, max_length=255, null=True),
        ),
    ]
