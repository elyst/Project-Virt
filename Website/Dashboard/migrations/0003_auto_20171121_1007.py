# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 10:07
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0002_auto_20171121_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='birthdate',
            field=models.DateField(default=datetime.datetime(2017, 11, 21, 10, 7, 15, 214982, tzinfo=utc), verbose_name='Geboortedatum'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='name',
            field=models.CharField(default='Voornaam', max_length=255, verbose_name='Voornaam'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='surname',
            field=models.CharField(default='Tussenvoegsel & Achternaam', max_length=255, verbose_name='Tussenvoegsel + Achternaam'),
        ),
    ]
