# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arm_settings', '0004_auto_20150826_1116'),
    ]

    operations = [
        migrations.AddField(
            model_name='authsettings',
            name='redirect_uri',
            field=models.CharField(default='http://127.0.0.1:8000/accesscode/', max_length=1000),
            preserve_default=False,
        ),
    ]
