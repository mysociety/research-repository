# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-06-13 11:06


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0033_auto_20180525_0930"),
    ]

    operations = [
        migrations.CreateModel(
            name="Site",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("site_title", models.CharField(default=b"", max_length=30)),
                (
                    "default_tag",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="repository.Tag",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="researchitem",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="items", to="repository.Tag"
            ),
        ),
    ]
