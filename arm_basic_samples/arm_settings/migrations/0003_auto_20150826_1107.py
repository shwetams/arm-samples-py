# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('arm_settings', '0002_authsettings_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authsettings',
            name='user_id',
            field=models.OneToOneField(related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
