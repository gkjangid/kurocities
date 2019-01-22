from    django.forms.models         import model_to_dict
from    django.http                 import Http404
from    django.views                import View
from    .base                       import cors_json_response, group_access
from    ..                          import models


class CheckerActivityAnswers_V1( View ):

    @group_access( 'KCT-Checker' )
    def get( self, request, resource_id=None, **kwargs ):
        user_activity_qs = ( models.UserActivity.objects
            .filter(
                activity__id = resource_id,
                invitation__isnull   = True,
                completed__isnull    = False,
                date_checked__isnull = True,
            )
            .order_by( 'completed', 'user__username' )
        )
        data     = []
        excludes = [ 'groups', 'user_permissions', 'password' ]
        for user_activity, ua in zip( user_activity_qs.values(), user_activity_qs ):
            user_activity ['user'] = model_to_dict( ua.user, exclude=excludes )
            data.append( user_activity )

        return cors_json_response( request, { 'data': data } )
