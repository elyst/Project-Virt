# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-27 12:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0006_auto_20171127_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='birthdate',
            field=models.DateField(default=datetime.datetime(2017, 11, 27, 12, 36, 3, 903326, tzinfo=utc), verbose_name='Geboortedatum'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='profilepic',
            field=models.ImageField(default='profiles/no-profile.png', upload_to='profiles/'),
        ),
    ]
