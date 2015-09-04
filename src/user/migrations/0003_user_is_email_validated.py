# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_email_validated',
            field=models.BooleanField(verbose_name='Is email validated', default=True, help_text='Designates whether this user has validated their email.'),
            preserve_default=True,
        ),
    ]
