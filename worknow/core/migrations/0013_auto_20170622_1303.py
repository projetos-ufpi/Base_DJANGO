# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-22 16:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20170622_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, upload_to='profile_image', verbose_name='Imagem de perfil'),
        ),
    ]