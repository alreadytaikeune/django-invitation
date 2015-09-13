# coding:utf-8
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from invitation.sample.models import EVENT_MODEL, AUTH_USER_MODEL, load_model_from_string
from invitation.models import Invitation, InvitationContext, Notification
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
        self.invitation.notifications.add(self.notification_day)
        self.invitation.notifications.add(self.notification_week)
        self.invitation.save()


    def test_accept_invitation(self):
        """
            Tests the accept method on InvitationModel.
            ..todo::tests the signals
        """
        # Default value of accepted is none
        self.assertIsNone(self.invitation.accepted)
        self.assertTrue(self.invitation.accept())
        # The accept action updated it.
        self.assertIsNotNone(self.invitation.accepted)


    def test_reject_invitation(self):
        """
            Tests the reject method on InvitationModel.
            ..todo::tests the signals
        """
        # Default value of rejected is none
        self.assertIsNone(self.invitation.rejected)
        self.assertTrue(self.invitation.reject())
        # The reject action updated it.
        self.assertIsNotNone(self.invitation.rejected)


    def test_mark_viewed_invitation(self):
        """
            Tests the mark_viewed method on InvitationModel.
            ..todo::tests the signals
        """
        # Default value of viewed is none
        self.assertIsNone(self.invitation.viewed)
        self.assertTrue(self.invitation.mark_viewed())
        # The view action updated it.
        self.assertIsNotNone(self.invitation.viewed)


    def test_find_invitations_to_notify(self):
        invitations = find_invitations_to_notify()
        # Tests that the invitation was returned.
        self.assertEqual(len(invitations),1)
        # Tests that the invitation was returned.
        self.assertEqual(invitations[0][0].id,self.invitation.id)
        # This is the shortest delay which has been taken into account.
        self.assertEqual(invitations[0][1],self.notification_day.duration.days * 86400 * 1000000)