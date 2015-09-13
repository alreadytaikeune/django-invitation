# coding:utf-8
from django.utils import timezone

from invitation.models import InvitationNotification, Invitation
from invitation.sample.models import EVENT_MODEL, AUTH_USER_MODEL, load_model_from_string
from invitation.signals import *

Event = load_model_from_string(EVENT_MODEL)

def find_invitations_to_notify():
    """
        Find invitation to notify and send the notification.

        ..todo::set older notifications to sent.
    """
    # Checks that there is at list one event in the future.
    events = Event.objects.filter(starts__gte=timezone.now)
    if len(events) > 0:
        # Gets invitations that have upcoming event AND
        # notifications as the same time. We fetch all the 
        # events and linked invitations. We run only notifications
        # which are current day notification. We take only upcoming
        # events and filter notifications so that:
        #       GROUP BY is to get one notification per invitation
        #       ORDER BY is to get shortest notification only
        invitations = Invitation.objects.raw(
            """ SELECT invit.*, notif.duration, invnot.id AS notif_id FROM invitation_invitation AS invit
                JOIN invitation_invitationnotification AS invnot 
                    ON invnot.invitation_id = invit.id 
                JOIN invitation_notification AS notif
                    ON notif.id = invnot.notification_id
                JOIN invitation_invitationcontext AS contex
                    ON contex.id = invit.context_id
                JOIN invitation_defaultevent AS event
                    ON event.id = contex.event_id
                WHERE event.starts > NOW()
                    AND (NOW() + INTERVAL notif.duration MICROSECOND) > event.starts
                    AND (NOW() + INTERVAL (notif.duration - 86400*1000000) MICROSECOND) < event.starts
                    AND invnot.sent = 0
                GROUP BY invit.id
                ORDER BY notif.duration ASC
                """)
        output = []
        # Send upcoming signal for these invitations.
        for invitation in invitations:
            invitation_upcoming.send(invitation)
            output.append((invitation,invitation.duration,))
        InvitationNotification.objects.filter(id__in=(invitation.notif_id for invitation in invitations)).update(sent=True)
        return output