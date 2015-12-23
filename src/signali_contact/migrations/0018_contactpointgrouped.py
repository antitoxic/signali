# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0017_auto_20151216_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPointGrouped',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('signali_contact.contactpoint',),
        ),
    ]
