# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 04:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20161205_0359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='points',
        ),
        migrations.AlterField(
            model_name='player',
            name='matchHistoryByOpponent',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='matchHistoryByTime',
            field=models.TextField(),
        ),
    ]