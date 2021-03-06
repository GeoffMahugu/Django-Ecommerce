# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-21 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_auto_20160921_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=120, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('stars', models.CharField(choices=[('5', '5'), ('4', '4'), ('3', '3'), ('2', '2'), ('3', '1')], default='5', max_length=100)),
                ('review', models.TextField()),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='variation',
            name='age',
            field=models.CharField(choices=[('Any', 'Any'), ('Children', 'Children'), ('Adult', 'Adult')], default='Any', max_length=100),
        ),
        migrations.AddField(
            model_name='variation',
            name='gender',
            field=models.CharField(choices=[('Unisex', 'Unisex'), ('Male', 'Male'), ('Female', 'Female')], default='Unisex', max_length=100),
        ),
        migrations.AlterField(
            model_name='variation',
            name='color',
            field=models.CharField(choices=[('DEFAULT', 'DEFAULT'), ('RED', 'RED'), ('BLUE', 'BLUE'), ('YELLOW', 'YELLOW'), ('ORANGE', 'ORANGE'), ('GREEN', 'GREEN'), ('PINK', 'PINK'), ('BLACK', 'BLACK'), ('WHITE', 'WHITE'), ('GREY', 'GREY')], default='DEFAULT', max_length=100),
        ),
    ]
