from django.conf.urls import url
from .                import consumers

websocket_urlpatterns = [
    url( r'^ws/invitation/(?P<invitation_id>\d+)/team/(?P<team_name>.+)/',      consumers.InvitationConsumer ),
    url( r'^ws/invitation/(?P<invitation_id>\d+)/user/(?P<user_id>\d+)/',       consumers.InvitationConsumer ),
    url( r'^ws/invitation/(?P<invitation_id>\d+)/',                             consumers.InvitationConsumer ),
]
