# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 16:47


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0005_auto_20170222_1628"),
    ]

    operations = [
        migrations.AddField(
            model_name="researchoutput",
            name="title",
            field=models.CharField(default="", max_length=200),
            preserve_default=False,
        ),
    ]
