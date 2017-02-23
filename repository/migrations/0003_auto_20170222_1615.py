# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-22 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_auto_20170222_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResearchOutput',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, help_text=b'If the output is a file we should host ourselves, upload it.', upload_to=b'outputs/')),
                ('url', models.URLField(blank=True, help_text=b'If the output is hosted elsewhere (like a journal), what is the URL?')),
            ],
        ),
        migrations.AlterField(
            model_name='researchitem',
            name='authors',
            field=models.ManyToManyField(help_text=b'Authors of this research item.', related_name='items', through='repository.ItemAuthor', to='repository.Person'),
        ),
        migrations.AddField(
            model_name='researchitem',
            name='documents',
            field=models.ManyToManyField(to='repository.ResearchOutput'),
        ),
    ]
