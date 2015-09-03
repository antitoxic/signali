# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0004_auto_20150903_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('email', models.EmailField(max_length=250, verbose_name='email')),
                ('last_notified_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Last notified at')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Added at')),
                ('contactpoint', models.ForeignKey(related_name='subscribers', to='signali_contact.ContactPoint')),
            ],
            options={
                'abstract': False,
                'verbose_name_plural': 'subscriber',
                'verbose_name': 'subscriber',
            },
            bases=(models.Model,),
        ),
    ]
