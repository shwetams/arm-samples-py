# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utilities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='defaultnetworksettings',
            name='setting_type_id',
            field=models.CharField(default=b'default', max_length=20),
        ),
    ]
