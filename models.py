#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  
#  Copyright 2015 anis <anis@anis-realm>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from invitation.signals import *
from django.conf import settings

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

EVENT_MODEL = getattr(settings, 'EVENT_MODEL', '')



class InviationManager(models.Manager):
	
	def invitations(self, user):
		return InvitationContext.objects.filter(inviter=user)
	
	def invited_to(self, user):
		return InvitationContext.objects.filter(invitation_set__invitee = user)
	
	def invitations_sent(self, event):
		return Invitations.objects.filter(context__event = event)
	
	def create_context(self, user, event):
		new_context = InvitationContext(inviter = user, event=event)
		new_context.save()
		return new_context
	
	def invite(self, user, context):
		new_invite = Invitation(context=context, invitee=user)
		new_invite.save()
		invitation_sent.send(self, context = context, to_user = user)
		return new_invite



"""
The class InvitationContext represents the set-up for an invitation: 
User u invites to Event e. Then this context is used in a invitation 
directed to specific persons. This way, the tables comply with the 
4NF standard (Boyce-Codd form + no non-trivial multi-values 
dependancies) which would not be the case with a single Invitation class 
because it would have to contain for each invitee to a given event, the 
same inviter and same event, whereas the invitee should be indepedent of 
the key (inviter, event).
"""
@python_2_unicode_compatible
class InvitationContext(models.Model):
	inviter = models.ForeignKey(AUTH_USER_MODEL, null=False)
	event = models.ForeignKey(EVENT_MODEL, null=False)
	created = models.DateTimeField(default=timezone.now)
	
	objects=InviationManager()
	
	class Meta:
		verbose_name = 'set-up for the invitation'
		verbose_name_plural = 'set-ups for the invitation'
		unique_together = ('inviter', 'event')
	
	def __str__(self):
		return "User {0} is inviting at {1}".format(self.inviter_id, self.event_id)
	



@python_2_unicode_compatible
class Invitation(models.Model):
	context = models.ForeignKey(InvitationContext, null=False)
	invitee = models.ForeignKey(AUTH_USER_MODEL, null=False)
	created = models.DateTimeField(default=timezone.now)
	accepted = models.DateTimeField(blank=True, null=True)
	rejected = models.DateTimeField(blank=True, null=True)
	viewed = models.DateTimeField(blank=True, null=True)

	objects=InviationManager()
	
	class Meta:
		verbose_name = 'invitation'
		verbose_name_plural = 'invitations'
		unique_together = ('context', 'invitee')
	
	def accept():
		self.accepted = timezone.now()
		self.save()
		invitation_accepted.send(sender = self, by_user=invitee, event=context.event)
		return True
	
	def reject():
		self.rejected = timezone.now()
		self.save()
		invitation_rejected.send(sender = self, by_user=invitee, event=context.event)
		return True
		
	
	def mark_viewed():
		self.viewed = timezone.now()
		self.save()
		invitation_viewed.send(sender = self)
		return True
		
	def __str__(self):
		return u'invitation for event %s' % self.context.event.name
		
	def __unicode__(self):
		return u'invitation for event %s' % self.context.event.name


