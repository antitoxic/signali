# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali', '0004_auto_20150910_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='title_short',
            field=models.CharField(default='', verbose_name='short title', max_length=250),
        ),
    ]
