# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2020-04-07 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ItemRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=254)),
                ('description', models.TextField(max_length=999)),
                ('budget', models.IntegerField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('contact', models.EmailField(max_length=254)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PastSold',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=254)),
                ('date_sold', models.DateTimeField(blank=True)),
                ('description', models.TextField()),
                ('starting_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('finish_price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('image', models.ImageField(upload_to='images')),
                ('edu_info', models.CharField(default='', max_length=300)),
            ],
        ),
    ]
