# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '__first__'),
        ('location', '__first__'),
        ('taxonomy', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPoint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, blank=True, verbose_name='slug')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('response_time', models.PositiveIntegerField(max_length=20, blank=True, verbose_name='response time', null=True)),
                ('is_multilingual', models.CharField(max_length=20, default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is multilingual')),
                ('is_response_guaranteed', models.CharField(max_length=20, default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='guarantees response')),
                ('is_verifiable', models.CharField(max_length=20, default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is verifiable')),
                ('is_confirmation_issued', models.CharField(max_length=20, default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is there a confirmation issued')),
                ('is_mobile_friendly', models.CharField(max_length=20, default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is mobile friendly')),
                ('is_final_destination', models.CharField(max_length=20, default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='is final destination')),
                ('is_anonymous_allowed', models.CharField(max_length=20, default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")], verbose_name='allows anonymous requests')),
                ('is_registration_required', models.BooleanField(default=False, verbose_name='required registration')),
                ('is_photo_required', models.BooleanField(default=False, verbose_name='photo registration')),
                ('is_esign_required', models.BooleanField(default=False, verbose_name='required e-signature')),
                ('is_name_required', models.BooleanField(default=False, verbose_name='required name')),
                ('is_email_required', models.BooleanField(default=False, verbose_name='required email')),
                ('is_pic_required', models.BooleanField(default=False, verbose_name='required personal indentification code')),
                ('is_address_required', models.BooleanField(default=False, verbose_name='required address')),
                ('is_location_required', models.BooleanField(default=False, verbose_name='required location')),
                ('category', models.ForeignKey(related_name='contact_points', to='taxonomy.Category', verbose_name='category')),
                ('keywords', models.ManyToManyField(related_name='contact_points', to='taxonomy.Keyword', verbose_name='keywords')),
                ('operational_area', models.ForeignKey(related_name='contact_points', to='location.Area', verbose_name='operational area')),
            ],
            options={
                'verbose_name': 'contact point',
                'verbose_name_plural': 'contact points',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactPointRating',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('criteria_guide', models.TextField(blank=True, verbose_name='What is this rating indicating?.', null=True)),
                ('contactpoint', models.ForeignKey(related_name='skills_portfolio', to='contact.ContactPoint')),
                ('rating', models.ForeignKey(related_name='talents_portfolio', to='feedback.Rating')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('email', models.EmailField(max_length=250, verbose_name='email')),
                ('address', models.OneToOneField(to='location.Area', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL)),
                ('operational_area', models.ForeignKey(related_name='organisations', to='location.Area', verbose_name='operational area', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='contactpointrating',
            unique_together=set([('contactpoint', 'rating')]),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='organisation',
            field=models.ForeignKey(related_name='contact_points', to='contact.Organisation', verbose_name='organisation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='ratings',
            field=models.ManyToManyField(to='feedback.Rating', verbose_name='Ratings', through='contact.ContactPointRating'),
            preserve_default=True,
        ),
    ]
