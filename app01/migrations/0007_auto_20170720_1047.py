# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-20 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_auto_20170718_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.ImageField(upload_to='static/imgs', verbose_name='头像'),
        ),
    ]
