# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 12:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VMID', models.CharField(max_length=255)),
                ('Name', models.CharField(max_length=255)),
                ('CPUCores', models.IntegerField()),
                ('RAMAmount', models.IntegerField()),
                ('DISKSize', models.IntegerField()),
            ],
        ),
    ]
