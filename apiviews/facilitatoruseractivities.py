from    django.forms.models         import model_to_dict
from    django.http                 import Http404
from    django.views                import View
from    .base                       import cors_json_response, group_access
from    ..                          import models


class FacilitatorUserActivities_V1( View ):

    @group_access( 'KCT-Inviter' )
    def get( self, request, resource_id, **kwargs ):
        queryset = ( models.UserActivity.objects
            .filter( invitation__id = resource_id )
            .order_by( 'user__username' )
        )

        data = []
        for user_activity, ua in zip( queryset.values(), queryset ):
            user_activity ['user'] = ua.user.username
            data.append( user_activity )

        return cors_json_response( request, { 'data': data } )

