# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-27 03:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gallery_photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photo',
            options={'ordering': ['-timestamp_posted']},
        ),
    ]
