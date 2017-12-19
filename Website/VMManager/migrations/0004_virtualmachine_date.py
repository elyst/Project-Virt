# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 11:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('VMManager', '0003_auto_20171211_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='virtualmachine',
            name='Date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]