# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import signali.uploads


class Migration(migrations.Migration):

    dependencies = [
        ('signali', '0005_setting_title_short'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='facebook_share',
            field=sorl.thumbnail.fields.ImageField(null=True, blank=True, verbose_name='facebook share image', upload_to=signali.uploads.Uploader('signali')),
        ),
    ]
