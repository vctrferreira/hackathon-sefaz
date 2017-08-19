# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-19 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_sefaz', '0002_auto_20170819_0503'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='cpf',
            field=models.CharField(max_length=15, unique=True, verbose_name='CPF'),
        ),
    ]