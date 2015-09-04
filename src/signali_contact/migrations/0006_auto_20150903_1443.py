# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signali_contact', '0005_auto_20150903_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactpoint',
            name='is_anonymous_allowed',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='allows anonymous requests', default='dontknow', blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='is_confirmation_issued',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is there a confirmation issued', default='dontknow', blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='is_final_destination',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is final destination', default='dontknow', blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='is_mobile_friendly',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is mobile friendly', default='dontknow', blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='is_multilingual',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is multilingual', default='dontknow', blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='is_response_guaranteed',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='guarantees response', default='dontknow', blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='is_verifiable',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is verifiable', default='dontknow', blank=True, max_length=20),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='contactpoint',
            name='organisation',
            field=models.ForeignKey(verbose_name='organisation', null=True, related_name='contact_points', to='signali_contact.Organisation'),
            preserve_default=True,
        ),
    ]
