# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-18 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='nickname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
