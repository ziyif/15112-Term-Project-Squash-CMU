# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 22:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20161125_2104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requirements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('min_level', models.DecimalField(choices=[(1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0), (5.5, 5.5), (6.0, 6.0)], decimal_places=1, max_digits=2)),
                ('max_level', models.DecimalField(choices=[(1.0, 1.0), (1.5, 1.5), (2.0, 2.0), (2.5, 2.5), (3.0, 3.0), (3.5, 3.5), (4.0, 4.0), (4.5, 4.5), (5.0, 5.0), (5.5, 5.5), (6.0, 6.0)], decimal_places=1, max_digits=2)),
                ('frequency', models.IntegerField(choices=[(1, 'Once/ week'), (2, 'Twice/ week'), (3, 'Three times/ week'), (4, 'Four times/ week'), (5, 'Five times/ week'), (6, 'Six times/ week'), (7, 'Everyday')])),
                ('times', models.TextField()),
            ],
        ),
    ]
