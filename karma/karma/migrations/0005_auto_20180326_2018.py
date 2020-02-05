# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-26 20:18
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('karma', '0004_auto_20171204_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='karmapoints',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]