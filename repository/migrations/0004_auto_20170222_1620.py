# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 16:20


from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0003_auto_20170222_1615"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="researchitem",
            name="documents",
        ),
        migrations.AddField(
            model_name="researchoutput",
            name="research_item",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="repository.ResearchItem",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="researchitem",
            name="authors",
            field=models.ManyToManyField(
                help_text=b"Authors of this research item.",
                through="repository.ItemAuthor",
                to="repository.Person",
            ),
        ),
    ]
