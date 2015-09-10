# coding:utf-8

from django.test import TestCase
from invitation.sample.models import EVENT_MODEL, AUTH_USER_MODEL, load_model_from_string
from invitation.models import Invitation, InvitationContext

User = load_model_from_string(AUTH_USER_MODEL)
Event = load_model_from_string(EVENT_MODEL)

class InvitationContextTest(TestCase):
    def createUser(self,username):
        user = User(username=username)
        user.save()
        return user

    def setUp(self):
        self.author = self.createUser(username="test_author")
        self.inviter = self.createUser(username="test_inviter")
        self.invitee = self.createUser(username="test_invitee")

        self.event = Event.create("Event name",self.author,
                                        "Some interesting place")
        self.event.save()

        self.invitation_context = InvitationContext(inviter=self.inviter, 
                                                    event=self.event)
        self.invitation_context.save()
        
        self.invitation = Invitation(context=self.invitation_context,
                                     invitee=self.invitee)
        self.invitation.save()
        
    def test_accept_invitation(self):
        pass

    def test_reject_invitation(self):
        pass

    def test_mark_viewed_invitation(self):
        pass