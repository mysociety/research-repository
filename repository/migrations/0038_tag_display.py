# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-13 16:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0037_researchitem_show_citation'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='display',
            field=models.BooleanField(default=True),
        ),
    ]