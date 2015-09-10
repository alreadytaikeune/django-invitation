# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('place', models.CharField(max_length=100, null=True, blank=True)),
                ('name', models.CharField(max_length=200)),
                ('starts', models.DateTimeField(default=b'', null=True, blank=True)),
                ('publisher', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('accepted', models.DateTimeField(null=True, blank=True)),
                ('rejected', models.DateTimeField(null=True, blank=True)),
                ('viewed', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'invitation',
                'verbose_name_plural': 'invitations',
            },
        ),
        migrations.CreateModel(
            name='InvitationContext',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('event', models.ForeignKey(to='invitation.DefaultEvent')),
                ('inviter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'set-up for the invitation',
                'verbose_name_plural': 'set-ups for the invitation',
            },
        ),
        migrations.AddField(
            model_name='invitation',
            name='context',
            field=models.ForeignKey(to='invitation.InvitationContext'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='invitee',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='invitationcontext',
            unique_together=set([('inviter', 'event')]),
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('context', 'invitee')]),
        ),
    ]
