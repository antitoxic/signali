# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Limit',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('action', models.CharField(db_index=True, max_length=255, verbose_name='action name')),
                ('count', models.PositiveIntegerField(default=0, verbose_name='visits')),
                ('last_executed_timestamp', models.PositiveIntegerField(null=True, verbose_name='unix timestamp of last successful action execution')),
                ('ip', models.GenericIPAddressField(null=True, verbose_name='ip address')),
                ('user', models.ForeignKey(related_name='rate_limits', verbose_name='user', to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
