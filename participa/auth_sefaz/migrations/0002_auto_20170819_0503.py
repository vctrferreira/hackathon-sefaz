# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-19 05:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_sefaz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('SU', 'Super User'), ('C', 'Common User')], default='C', max_length=2, verbose_name='Tipo do usuário'),
        ),
    ]
