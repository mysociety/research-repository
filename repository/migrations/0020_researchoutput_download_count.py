# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-04 13:06


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0019_auto_20170626_1620"),
    ]

    operations = [
        migrations.AddField(
            model_name="researchoutput",
            name="download_count",
            field=models.IntegerField(default=0),
        ),
    ]
