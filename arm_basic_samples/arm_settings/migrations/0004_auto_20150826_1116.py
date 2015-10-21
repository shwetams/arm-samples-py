# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('arm_settings', '0003_auto_20150826_1107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authsettings',
            name='user_id',
            field=models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]
