# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0006_remove_invitation_notifications'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invitation',
            old_name='notifications2',
            new_name='notifications',
        ),
    ]
