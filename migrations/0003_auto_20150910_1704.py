# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0002_auto_20150910_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitationcontext',
            name='notifications',
        ),
        migrations.AddField(
            model_name='invitation',
            name='notifications',
            field=models.ManyToManyField(to='invitation.Notification', blank=True),
        ),
    ]
