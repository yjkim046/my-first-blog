# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-13 07:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thread_no',
            field=models.IntegerField(default=1),
        ),
    ]
