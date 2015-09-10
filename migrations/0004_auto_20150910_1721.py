# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0003_auto_20150910_1704'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notification',
            old_name='time',
            new_name='duration',
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('duration',)]),
        ),
    ]
