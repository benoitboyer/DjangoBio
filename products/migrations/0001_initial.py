# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 10:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_brand', models.CharField(max_length=50)),
                ('product_article_code', models.CharField(max_length=20)),
                ('product_code', models.IntegerField()),
                ('product_name', models.CharField(max_length=150)),
                ('product_unit_packaging_number', models.IntegerField(default=1)),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('product_selected', models.BooleanField(default=False)),
            ],
        ),
    ]
