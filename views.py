# coding:utf-8
from django.utils import timezone

from invitation.models import Notification, Invitation, InvitationContext
from invitation.sample.models import EVENT_MODEL, AUTH_USER_MODEL, load_model_from_string
from invitation.signals import *

Event = load_model_from_string(EVENT_MODEL)

def find_invitations_to_notify():
    # Checks that there is at list one event in the future.
    events = Event.objects.filter(starts__gte=timezone.now)
    if len(events) > 0:
        # Gets invitations that have upcoming event AND
        # notifications as the same time. We fetch all the 
        # events and linked invitations. We take only upcoming
        # events and filter notifications so that:
        #       GROUP BY is to get one notification per invitation
        #       ORDER BY is to get shortest notification only
        invitations = Invitation.objects.raw(
            """ SELECT * FROM invitation_invitation AS invit
                JOIN invitation_invitation_notifications AS invnot 
                    ON invnot.invitation_id = invit.id 
                JOIN invitation_notification AS notif
                    ON notif.id = invnot.notification_id
                JOIN invitation_invitationcontext AS contex
                    ON contex.id = invit.context_id
                JOIN invitation_defaultevent AS event
                    ON event.id = contex.event_id
                WHERE event.starts > NOW()
                    AND (NOW() + INTERVAL notif.duration MICROSECOND) > event.starts
                GROUP BY invit.id
                ORDER BY notif.duration ASC
                """)
        # Send upcoming signal for these invitations.
        for invitation in invitations:
            invitation_upcoming.send(invitation)