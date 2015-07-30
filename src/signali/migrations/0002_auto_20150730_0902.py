# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
        ('taxonomy', '0003_remove_keyword_style'),
        ('location', '0001_initial'),
        ('signali', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('location.area',),
        ),
        migrations.CreateModel(
            name='CategoryProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('taxonomy.category',),
        ),
        migrations.CreateModel(
            name='ContactPointProxy',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('contact.contactpoint',),
        ),
        migrations.AlterModelOptions(
            name='visibility',
            options={'verbose_name_plural': 'visibility options', 'verbose_name': 'visibility'},
        ),
        migrations.AddField(
            model_name='visibility',
            name='area',
            field=models.OneToOneField(related_name='visibility', to='location.Area', blank=True, null=True, verbose_name='area'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='visibility',
            name='keyword',
            field=models.OneToOneField(related_name='visibility', to='taxonomy.Keyword', blank=True, null=True, verbose_name='keyword'),
            preserve_default=True,
        ),
    ]
