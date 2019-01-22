from    django.db.models            import Q
from    django.http                 import Http404, HttpResponse
from    django.views                import View

from    ..                          import models
from    .base                       import cors_json_response


class UserActivityChatMessage_V1( View ):

    def get( self, request, resource_id ):
        try:
            user_activity = models.UserActivity.objects.get( pk=int( resource_id ), user = request.user )
        except models.UserActivity.DoesNotExist:
            return HttpResponse( 'UCM: 1', status=400 )
        if not user_activity.invitation:
            return HttpResponse( 'UCM: 2', status=400 )

        query = models.ChatMessage.objects.filter( invitation = user_activity.invitation )
        if not user_activity.team:
            query = query.filter( Q( team = '' ) )
        else:
            query = query.filter( Q( team = '' ) | Q( team = user_activity.team ) )
        data = []
        for values, obj in zip( query.values(), query ):
            values ['fromUser'] = obj.user.username
            data.append( values )
        return cors_json_response( request, { 'data': data } )
