# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arm_settings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='authsettings',
            name='user_id',
            field=models.ForeignKey(related_name='user_id', default=1, to=settings.AUTH_USER_MODEL, unique=True),
            preserve_default=False,
        ),
    ]
