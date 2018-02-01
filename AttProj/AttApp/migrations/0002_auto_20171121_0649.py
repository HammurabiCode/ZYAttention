# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-21 06:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AttApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='score',
            name='date_time',
        ),
        migrations.AddField(
            model_name='score',
            name='test',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='AttApp.Test'),
            preserve_default=False,
        ),
    ]