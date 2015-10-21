# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_type', models.CharField(default=b'A', max_length=1, choices=[(b'A', b'Application'), (b'U', b'User based')])),
                ('client_id', models.CharField(max_length=1000)),
                ('tenant_id', models.CharField(max_length=1000)),
                ('client_secret', models.CharField(max_length=1000, blank=True)),
            ],
        ),
    ]
