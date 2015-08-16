# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import signali.uploads
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('signali', '0003_visibility_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='visibility',
            name='cover',
            field=sorl.thumbnail.fields.ImageField(null=True, blank=True, verbose_name='cover', upload_to=signali.uploads.Uploader('visibility')),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='visibility',
            name='preview',
            field=sorl.thumbnail.fields.ImageField(null=True, blank=True, verbose_name='preview', upload_to=signali.uploads.Uploader('visibility')),
            preserve_default=True,
        ),
    ]
