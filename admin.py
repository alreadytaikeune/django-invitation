# -*- coding: utf-8 -*-
from django.contrib import admin
from django.conf import settings

from invitation.models import *
from invitation.sample.models import EVENT_MODEL, load_model_from_string

class ContextAdmin(admin.ModelAdmin):
	model = InvitationContext
	list_display = ('inviter', 'related_event')
	def related_event(self, obj):
		return unicode(obj.event.name)


class InvitationAdmin(admin.ModelAdmin):
	model = Invitation
	list_display = ('related_context', 'invitee', 'created', 'accepted')
	def related_context(self, obj):
		return unicode(obj.context.event.name)
	related_context.short_descrption="Set-up"


admin.site.register(InvitationContext, ContextAdmin)
admin.site.register(Invitation, InvitationAdmin)
admin.site.register(Notification)

Event = load_model_from_string(EVENT_MODEL)
admin.site.register(Event)
