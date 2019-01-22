from    django.http                 import Http404, HttpResponseForbidden
from    django.views                import View
from    .base                       import cors_json_response, get_post_data
from    ..                          import models


class UserActivityTeam_V1( View ):

    def post( self, request, **kwargs ):
        data = get_post_data( request )
        user_activity = models.UserActivity.objects.get( pk = data ['id'] )
        if int( data ['user_id'] ) != user_activity.user.id:
            return HttpResponseForbidden
        if user_activity.completed or not user_activity.invitation:
            return HttpResponseForbidden
        team = data ['team']
        user_activity.team = team
        user_activity.save()
        return cors_json_response( request, { 'data': team })
