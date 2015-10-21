# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arm_settings', '0005_authsettings_redirect_uri'),
    ]

    operations = [
        migrations.AddField(
            model_name='authsettings',
            name='subscription_id',
            field=models.CharField(max_length=1000, blank=True),
        ),
    ]
