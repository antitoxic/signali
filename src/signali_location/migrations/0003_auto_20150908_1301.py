# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('signali_location', '0002_auto_20150906_0200'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='level',
            field=models.PositiveIntegerField(default=0, db_index=True, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='area',
            name='lft',
            field=models.PositiveIntegerField(default=0, db_index=True, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='area',
            name='rght',
            field=models.PositiveIntegerField(default=0, db_index=True, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='area',
            name='tree_id',
            field=models.PositiveIntegerField(default=0, db_index=True, editable=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='area',
            name='parent',
            field=mptt.fields.TreeForeignKey(related_name='children', verbose_name='parent area', null=True, blank=True, to='signali_location.Area'),
        ),
    ]
