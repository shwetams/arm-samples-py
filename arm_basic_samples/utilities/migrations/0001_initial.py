# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultNetworkSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_subnet_name', models.CharField(max_length=24, blank=True)),
                ('default_address_range', models.CharField(max_length=100, blank=True)),
                ('default_address_space', models.CharField(max_length=100, blank=True)),
            ],
        ),
    ]
