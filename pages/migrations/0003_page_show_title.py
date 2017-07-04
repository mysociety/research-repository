# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 13:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20170223_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='show_title',
            field=models.BooleanField(default=True, help_text=b'Should the template display the page title as well as the content?'),
        ),
    ]