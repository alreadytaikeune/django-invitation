# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invitation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('time', models.DurationField()),
            ],
            options={
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
            },
        ),
        migrations.AlterUniqueTogether(
            name='notification',
            unique_together=set([('time',)]),
        ),
        migrations.AddField(
            model_name='invitationcontext',
            name='notifications',
            field=models.ManyToManyField(to='invitation.Notification', null=True),
        ),
    ]
