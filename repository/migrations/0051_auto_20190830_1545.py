# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-30 14:45


from django.db import migrations, models
import repository.models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0050_researchitem_zip_archive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='researchitem',
            name='zip_archive',
            field=models.FileField(blank=True, help_text=b'Upload a stringprint document as a zip', null=True, storage=repository.models.OverwriteStorage(), upload_to=b'zips/'),
        ),
    ]