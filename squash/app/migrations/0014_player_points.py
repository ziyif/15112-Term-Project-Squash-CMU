# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 04:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20161205_0405'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='points',
            field=models.IntegerField(null=True),
        ),
    ]