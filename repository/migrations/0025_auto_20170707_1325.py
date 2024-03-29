# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-07 12:25


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0024_auto_20170705_1522"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="hero",
            field=models.ImageField(
                blank=True,
                help_text=b"A hero image which will be displayed on this tag's page. Recommended ratio is 1024x350.",
                null=True,
                upload_to=b"hero/",
            ),
        ),
        migrations.AlterField(
            model_name="taggroup",
            name="hero",
            field=models.ImageField(
                blank=True,
                help_text=b"A hero image which will be displayed on this tag group's page. Recommended ratio is 1024x350.",
                null=True,
                upload_to=b"hero/",
            ),
        ),
    ]
