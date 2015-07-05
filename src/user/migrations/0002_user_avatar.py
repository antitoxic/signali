# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(null=True, blank=True, verbose_name='avatar', upload_to=user.models.user_file_name),
            preserve_default=True,
        ),
    ]
