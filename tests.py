# coding:utf-8
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from invitation.sample.models import EVENT_MODEL, AUTH_USER_MODEL, load_model_from_string
from invitation.models import Invitation, InvitationNotification, InvitationContext, Notification
from invitation.views import find_invitations_to_notify
from invitation.signals import * 

User = load_model_from_string(AUTH_USER_MODEL)
Event = load_model_from_string(EVENT_MODEL)

class InvitationTest(TestCase):
    def createUser(self,username):
        user = User(username=username)
        user.save()
        return user

    def setUp(self):
        self.author = self.createUser(username="test_author")
        self.inviter = self.createUser(username="test_inviter")
        self.invitee = self.createUser(username="test_invitee")


        self.notification_day = Notification(name="1 day",
                                     duration=timedelta(days=1))
        self.notification_day.save()

        self.notification_week = Notification(name="7 day",
                                     duration=timedelta(days=7))
        self.notification_week.save()
        
        self.event = Event.create("Event name",self.author,
                                        "Some interesting place")
        self.event.starts = timezone.now() + timedelta(hours=23)
        self.event.save()

        self.invitation_context = InvitationContext(inviter=self.inviter, 
                                                    event=self.event)
        self.invitation_context.save()
        
        self.invitation = Invitation(context=self.invitation_context,
                                     invitee=self.invitee)
        self.invitation.save()

        self.invitation_notification_day = InvitationNotification(
                                        invitation=self.invitation,
                                        notification=self.notification_day)
        self.invitation_notification_week = InvitationNotification(
                                        invitation=self.invitation,
                                        notification=self.notification_week)
        self.invitation_notification_day.save()
        self.invitation_notification_week.save()

        self.signal_by_user = None
        self.signal_event = None
        self.signal_listened = False


    def test_accept_invitation(self):
        """
            Tests the accept method on InvitationModel.
        """
        def invitation_accepted_listener(sender, by_user, event, **kwargs):
            self.signal_by_user = by_user
            self.signal_event = event
        
        # Connects to the signal
        invitation_accepted.connect(invitation_accepted_listener, sender=self.invitation)
        
        # Default value of accepted is none then accepts it
        self.assertIsNone(self.invitation.accepted)
        self.assertTrue(self.invitation.accept())

        # The accept action updated it.
        self.assertIsNotNone(self.invitation.accepted)

        # Tests that the signal has been sent and received.
        self.assertEqual(self.invitee, self.signal_by_user)
        self.assertEqual(self.event, self.signal_event)


    def test_reject_invitation(self):
        """
            Tests the reject method on InvitationModel.
        """
        def invitation_rejected_listener(sender, by_user, event, **kwargs):
            self.signal_by_user = by_user
            self.signal_event = event
        
        # Connects to the signal
        invitation_rejected.connect(invitation_rejected_listener, sender=self.invitation)

        # Default value of rejected is none then rejects it
        self.assertIsNone(self.invitation.rejected)
        self.assertTrue(self.invitation.reject())

        # The reject action updated it.
        self.assertIsNotNone(self.invitation.rejected)

        # Tests that the signal has been sent and received.
        self.assertEqual(self.invitee, self.signal_by_user)
        self.assertEqual(self.event, self.signal_event)

    def test_mark_viewed_invitation(self):
        """
            Tests the mark_viewed method on InvitationModel.
        """
        def invitation_viewed_listener(sender, **kwargs):
            self.signal_listened = True

        # Connects to the signal
        invitation_viewed.connect(invitation_viewed_listener, sender=self.invitation)
        
        # Default value of viewed is none
        self.assertIsNone(self.invitation.viewed)
        self.assertTrue(self.invitation.mark_viewed())

        # The view action updated it.
        self.assertIsNotNone(self.invitation.viewed)
        
        # Tests that the signal has been sent and received.
        self.assertTrue(self.signal_listened)

    def test_find_invitations_to_notify(self):
        invitations = find_invitations_to_notify()
        # Tests that the invitation was returned.
        self.assertEqual(len(invitations),1)
        # Tests that the invitation was returned.
        self.assertEqual(invitations[0][0].id,self.invitation.id)
        # This is the shortest delay which has been taken into account.
        self.assertEqual(invitations[0][1],self.notification_day.duration.days * 86400 * 1000000)

        # Checks hat the notification has been set to sent !
        try:
            invitation_notification = InvitationNotification.objects.get(id=self.invitation_notification_day.id)
        except InvitationNotification.DoesNotExist:
            invitation_notification = None
        self.assertIsNotNone(invitation_notification)
        self.assertTrue(invitation_notification.sent)