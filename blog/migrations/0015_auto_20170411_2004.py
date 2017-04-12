# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-12 03:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20170411_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='post',
        ),
        migrations.AddField(
            model_name='comment',
            name='approved_comment',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]
