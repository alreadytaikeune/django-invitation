# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0004_auto_20150910_1721'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitationNotification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sent', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'notification for invitation',
                'verbose_name_plural': 'notifications for invitations',
            },
        ),
        migrations.AlterField(
            model_name='invitation',
            name='notifications',
            field=models.ManyToManyField(related_name='+', to='invitation.Notification', blank=True),
        ),
        migrations.AddField(
            model_name='invitationnotification',
            name='invitation',
            field=models.ForeignKey(to='invitation.Invitation'),
        ),
        migrations.AddField(
            model_name='invitationnotification',
            name='notification',
            field=models.ForeignKey(to='invitation.Notification'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='notifications2',
            field=models.ManyToManyField(to='invitation.Notification', through='invitation.InvitationNotification', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='invitationnotification',
            unique_together=set([('invitation', 'notification')]),
        ),
    ]
