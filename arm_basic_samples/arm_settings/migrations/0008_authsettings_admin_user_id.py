# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arm_settings', '0007_authsettings_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='authsettings_admin',
            name='user_id',
            field=models.CharField(default=b'Admin', unique=True, max_length=5),
        ),
    ]
