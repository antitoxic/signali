# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0011_contactpoint_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpoint',
            name='email',
            field=models.EmailField(verbose_name='Email', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='slug',
            field=models.SlugField(verbose_name='slug', max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='url',
            field=models.URLField(verbose_name='URL', max_length=255, null=True, blank=True),
        ),
    ]
