# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20170621_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='telefone',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]
