# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import signali.uploads
import django.utils.timezone
import sorl.thumbnail.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('signali_taxonomy', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('signali_location', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('popularity', models.PositiveIntegerField(verbose_name='popularity', default=0)),
                ('views', models.PositiveIntegerField(verbose_name='popularity', default=0)),
                ('is_featured', models.BooleanField(verbose_name='is featured', default=False)),
                ('is_public', models.BooleanField(verbose_name='is public', default=False)),
                ('style', models.CharField(max_length=255, verbose_name='Style [technical]', null=True, blank=True)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, verbose_name='slug', blank=True)),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('is_multilingual', models.CharField(max_length=20, verbose_name='is multilingual', default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")])),
                ('is_response_guaranteed', models.CharField(max_length=20, verbose_name='guarantees response', default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")])),
                ('is_verifiable', models.CharField(max_length=20, verbose_name='is verifiable', default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")])),
                ('is_confirmation_issued', models.CharField(max_length=20, verbose_name='is there a confirmation issued', default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")])),
                ('is_mobile_friendly', models.CharField(max_length=20, verbose_name='is mobile friendly', default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")])),
                ('is_final_destination', models.CharField(max_length=20, verbose_name='is final destination', default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")])),
                ('is_anonymous_allowed', models.CharField(max_length=20, verbose_name='allows anonymous requests', default='dontknow', choices=[('yes', 'Yes'), ('no', 'No'), ('dontknow', "I don't know")])),
                ('is_registration_required', models.BooleanField(verbose_name='required registration', default=False)),
                ('is_photo_required', models.BooleanField(verbose_name='photo registration', default=False)),
                ('is_esign_required', models.BooleanField(verbose_name='required e-signature', default=False)),
                ('is_name_required', models.BooleanField(verbose_name='required name', default=False)),
                ('is_email_required', models.BooleanField(verbose_name='required email', default=False)),
                ('is_pic_required', models.BooleanField(verbose_name='required personal indentification code', default=False)),
                ('is_address_required', models.BooleanField(verbose_name='required address', default=False)),
                ('is_location_required', models.BooleanField(verbose_name='required location', default=False)),
                ('preview', sorl.thumbnail.fields.ImageField(verbose_name='preview', upload_to=signali.uploads.Uploader('visibility'), null=True, blank=True)),
                ('cover', sorl.thumbnail.fields.ImageField(verbose_name='cover', upload_to=signali.uploads.Uploader('visibility'), null=True, blank=True)),
                ('category', models.ForeignKey(verbose_name='category', related_name='contact_points', to='signali_taxonomy.Category')),
                ('keywords', models.ManyToManyField(verbose_name='keywords', related_name='contact_points', to='signali_taxonomy.Keyword')),
                ('operational_area', models.ForeignKey(verbose_name='operational area', related_name='contact_points', to='signali_location.Area')),
            ],
            options={
                'verbose_name': 'contact point',
                'verbose_name_plural': 'contact points',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organisation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('popularity', models.PositiveIntegerField(verbose_name='popularity', default=0)),
                ('views', models.PositiveIntegerField(verbose_name='popularity', default=0)),
                ('is_featured', models.BooleanField(verbose_name='is featured', default=False)),
                ('is_public', models.BooleanField(verbose_name='is public', default=False)),
                ('style', models.CharField(max_length=255, verbose_name='Style [technical]', null=True, blank=True)),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('email', models.EmailField(max_length=250, verbose_name='email')),
                ('preview', sorl.thumbnail.fields.ImageField(verbose_name='preview', upload_to=signali.uploads.Uploader('visibility'), null=True, blank=True)),
                ('cover', sorl.thumbnail.fields.ImageField(verbose_name='cover', upload_to=signali.uploads.Uploader('visibility'), null=True, blank=True)),
                ('address', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='signali_location.Area')),
                ('operational_area', models.ForeignKey(verbose_name='operational area', related_name='organisations', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='signali_location.Area')),
            ],
            options={
                'verbose_name': 'organisation',
                'verbose_name_plural': 'organisations',
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SignalContactPointFeedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('usability', models.PositiveIntegerField(max_length=2, verbose_name='Usability', null=True, choices=[(1, 'Weak'), (2, 'Could be better'), (3, 'Adequate'), (4, 'Good'), (5, 'Excellent')], blank=True)),
                ('response_speed', models.PositiveIntegerField(max_length=2, verbose_name='Response speed', null=True, choices=[(1, 'Weak'), (2, 'Could be better'), (3, 'Adequate'), (4, 'Good'), (5, 'Excellent')], blank=True)),
                ('added_at', models.DateTimeField(verbose_name='added at', default=django.utils.timezone.now)),
                ('comment', models.TextField(verbose_name='description', null=True, blank=True)),
                ('contactpoint', models.ForeignKey(to='signali_contact.ContactPoint', related_name='feedback')),
                ('user', models.ForeignKey(verbose_name='voter', related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contactpoint',
            name='organisation',
            field=models.ForeignKey(verbose_name='organisation', related_name='contact_points', to='signali_contact.Organisation'),
            preserve_default=True,
        ),
    ]
