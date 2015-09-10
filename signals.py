# coding:utf-8
from django.dispatch import Signal


invitation_context_created = Signal()
invitation_sent = Signal(providing_args=['context', 'to_user'])
invitation_rejected = Signal(providing_args=['by_user', 'event'])
invitation_accepted = Signal(providing_args=['by_user', 'event'])
invitation_viewed = Signal()
invitation_incoming = Signal()
