# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 04:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20161205_0431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='points',
            field=models.IntegerField(choices=[(1, 'Once/ week'), (2, 'Twice/ week'), (3, 'Three times/ week'), (4, 'Four times/ week'), (5, 'Five times/ week'), (6, 'Six times/ week'), (7, 'Everyday')], default=5),
        ),
    ]
