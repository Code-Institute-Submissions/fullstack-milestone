# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-03-28 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('antiques', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='antiques',
            name='edu_info',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='antiques',
            name='description',
            field=models.TextField(default=''),
        ),
    ]