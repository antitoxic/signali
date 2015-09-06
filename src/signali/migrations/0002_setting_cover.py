# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import signali.uploads


class Migration(migrations.Migration):

    dependencies = [
        ('signali', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='cover',
            field=sorl.thumbnail.fields.ImageField(verbose_name='cover', null=True, upload_to=signali.uploads.Uploader('signali'), blank=True),
        ),
    ]
