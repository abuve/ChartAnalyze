# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-11-09 07:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0002_auto_20181109_1426'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datasetfield',
            old_name='name',
            new_name='alias',
        ),
    ]
