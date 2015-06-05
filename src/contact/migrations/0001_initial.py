# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPoint',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('slug', models.SlugField(blank=True, verbose_name='slug', max_length=255)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('response_time', models.PositiveIntegerField(null=True, blank=True, verbose_name='response time', max_length=20)),
                ('is_multilingual', models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is multilingual', default='dontknow')),
                ('is_response_guaranteed', models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='guarantees response', default='dontknow')),
                ('is_verifiable', models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is verifiable', default='dontknow')),
                ('is_confirmation_issued', models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is there a confirmation issued', default='dontknow')),
                ('is_mobile_friendly', models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is mobile friendly', default='dontknow')),
                ('is_final_destination', models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is final destination', default='dontknow')),
                ('is_anonymous_allowed', models.CharField(max_length=20, choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='allows anonymous requests', default='dontknow')),
                ('is_registration_required', models.BooleanField(verbose_name='required registration', default=False)),
                ('is_photo_required', models.BooleanField(verbose_name='photo registration', default=False)),
                ('is_esign_required', models.BooleanField(verbose_name='required e-signature', default=False)),
                ('is_name_required', models.BooleanField(verbose_name='required name', default=False)),
                ('is_email_required', models.BooleanField(verbose_name='required email', default=False)),
                ('is_pic_required', models.BooleanField(verbose_name='required personal indentification code', default=False)),
                ('is_address_required', models.BooleanField(verbose_name='required address', default=False)),
                ('is_location_required', models.BooleanField(verbose_name='required location', default=False)),
                ('category', models.ForeignKey(verbose_name='category', related_name='contact_points', to='taxonomy.Category')),
                ('keywords', models.ManyToManyField(verbose_name='keywords', related_name='contact_points', to='taxonomy.Keyword')),
            ],
            options={
                'verbose_name': 'contact point',
                'verbose_name_plural': 'contact points',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactPointRequirement',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('contact_point', models.ForeignKey(verbose_name='contact point', related_name='requirements', to='contact.ContactPoint')),
            ],
            options={
                'verbose_name': 'contact point requirement',
                'verbose_name_plural': 'contact point requirements',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Orgаnisation',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=250)),
                ('email', models.EmailField(verbose_name='email', max_length=250)),
                ('address', models.TextField(blank=True, verbose_name='address')),
                ('city', models.TextField(blank=True, verbose_name='city')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='organisation',
            field=models.ForeignKey(verbose_name='organisation', related_name='contact_points', to='contact.Orgаnisation'),
            preserve_default=True,
        ),
    ]
