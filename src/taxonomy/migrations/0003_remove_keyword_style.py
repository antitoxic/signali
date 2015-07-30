# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0002_auto_20150711_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='keyword',
            name='style',
        ),
    ]
