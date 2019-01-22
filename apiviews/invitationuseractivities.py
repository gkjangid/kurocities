from    django.forms.models         import model_to_dict
from    django.http                 import Http404
from    django.views                import View
from    .base                       import cors_json_response, group_access
from    ..                          import models


class InvitationUserActivities_V1( View ):

    @group_access( 'KCT-Activity-Data' )
    def get( self, request, resource_id=None, **kwargs ):
        if not resource_id: raise Http404
        queryset = models.Invitation.objects.filter( pk = resource_id )
        if not queryset.count() == 1:
            raise Http404( 'IA: 1' )
        invitation = list( queryset )[0]
        user_activity_qs = ( models.UserActivity.objects
            .filter( invitation = invitation )
            .order_by( 'team', 'user__username' )
        )
        data = []
        excludes = [ 'groups', 'user_permissions', 'password' ]
        for user_activity, ua in zip( user_activity_qs.values(), user_activity_qs ):
            user_activity ['user']    = model_to_dict( ua.user, exclude=excludes )
            data.append( user_activity )

        return cors_json_response( request, { 'data': data } )
