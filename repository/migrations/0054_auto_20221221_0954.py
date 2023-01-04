# Generated by Django 3.2.16 on 2022-12-21 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("repository", "0053_tag_front_page_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="front_page_order",
            field=models.IntegerField(
                default=0,
                help_text="zero if not on front page, otherwise ascending order down the page",
            ),
        ),
        migrations.CreateModel(
            name="SearchItem",
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
                ("title", models.CharField(max_length=255)),
                ("url", models.CharField(max_length=1020)),
                ("text", models.TextField()),
                (
                    "research_item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="search_items",
                        to="repository.researchitem",
                    ),
                ),
            ],
        ),
    ]
