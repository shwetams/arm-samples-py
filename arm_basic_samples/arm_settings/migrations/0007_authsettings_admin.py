# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arm_settings', '0006_authsettings_subscription_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthSettings_Admin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client_id', models.CharField(max_length=1000)),
                ('tenant_id', models.CharField(max_length=1000)),
                ('redirect_uri', models.CharField(max_length=1000)),
                ('client_secret', models.CharField(max_length=1000, blank=True)),
                ('subscription_id', models.CharField(max_length=1000, blank=True)),
            ],
        ),
    ]
