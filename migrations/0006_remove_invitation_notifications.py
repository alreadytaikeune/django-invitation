# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0005_auto_20150913_1202'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='notifications',
        ),
    ]
