from django.conf.urls import include, url
from invitation.views import *
urlpatterns=[
url(r'invitation/createcontext', create_context), # takes as GET/POST parameters the event id
url(r'invitation/invite', invite), # takes as GET/POST parameters the context id as well as the invitee id
url(r'invitation/accept/(?P<invit_id>\d+)', accept),
url(r'invitation/reject/(?P<invit_id>\d+)', reject),
url(r'invitation/accepts', accepts),
url(r'invitation/rejects', rejects),
]
