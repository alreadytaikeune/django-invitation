# coding:utf-8
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

"""
The following models are only sample models to run the app. You can 
replace them with your own model simply by editing the
"""
class DefaultEvent(models.Model): 
    """
        Default Event model for example.
        .. todo:: add parameters to constructors to limit data
    """
    publisher = models.ForeignKey(AUTH_USER_MODEL, null=False)
    place = models.CharField(max_length=100, blank=True, null=True)
    name = models.CharField(max_length=200, null=False)
    starts = models.DateTimeField(null=True, blank=True, default=timezone.now)

    @classmethod
    def create(cls, name, publisher, place):
        event = cls(name=name, publisher=publisher,place=place)
        return event

EVENT_MODEL = getattr(settings, 'EVENT_MODEL', 'invitation.DefaultEvent')

def load_model_from_string(model_name):
    app_label,model_name = model_name.split(".",1)
    return apps.get_model(app_label=app_label,model_name=model_name)
