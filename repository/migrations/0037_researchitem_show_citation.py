# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-13 12:56


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0036_auto_20180613_1330"),
    ]

    operations = [
        migrations.AddField(
            model_name="researchitem",
            name="show_citation",
            field=models.BooleanField(default=True),
        ),
    ]
