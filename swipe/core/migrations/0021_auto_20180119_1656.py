# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-19 11:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20180119_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='emp_response',
            field=models.CharField(default='No Response', max_length=255),
        ),
    ]