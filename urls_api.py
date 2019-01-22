from django.conf.urls                   import url, include
from django.contrib.auth.decorators     import login_required
from .apiviews                          import views
import logging


api_patterns = [
    url(
        r'^(?P<resource>ActivityQuery)/(?P<query_type>\w+)/$',
        login_required( views.Api.as_view() ),
        name='api_activity_query',
    ),
    url(
        r'^(?P<resource>ActivityQuery)/$',
        login_required( views.Api.as_view() ),
        name='api_activity_query',
    ),

    url(
        r'^(?P<resource>mygroups)/$',
        login_required( views.Api.as_view() ),
        name='api_my_grooups'
    ),

    url( r'^(?P<resource>\w+)/(?P<resource_id>\w+)/(?P<sub_resource_id>\w+)/$', login_required( views.Api.as_view() ), name='api' ),
    url( r'^(?P<resource>\w+)/(?P<resource_id>\w+)/$',                          login_required( views.Api.as_view() ), name='api' ),
    url( r'^(?P<resource>\w+)/$',                                               login_required( views.Api.as_view() ), name='api' ),
]

urlpatterns = [
    url( r'login/$',             views.Login_V1.as_view(), name='api_login' ),
    url( r'^v(?P<version>\d+)/', include( api_patterns ) ),
]
