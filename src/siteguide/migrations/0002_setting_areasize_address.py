# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
        ('siteguide', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='areasize_address',
            field=models.ForeignKey(default=2, to='location.AreaSize', verbose_name='Which size denotes address-level area'),
            preserve_default=False,
        ),
    ]
