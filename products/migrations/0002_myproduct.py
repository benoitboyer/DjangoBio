# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-27 13:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyProduct',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
            },
            bases=('products.product',),
        ),
    ]