# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali', '0003_partner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'verbose_name': 'partner', 'ordering': ['order'], 'verbose_name_plural': 'partners'},
        ),
        migrations.AlterField(
            model_name='partner',
            name='provides',
            field=models.CharField(verbose_name='provides', max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='url',
            field=models.URLField(verbose_name='url', max_length=250),
        ),
    ]
