from    django.http                 import Http404, HttpResponse
from    django.views                import View

from    ..                          import models
from    .base                       import cors_json_response


class InvitationChatMessage_V1( View ):

    def get( self, request, resource_id ):
        try:
            invitation = models.Invitation.objects.get( pk=int( resource_id ) )
        except models.Invitation.DoesNotExist:
            return HttpResponse( 'ICM: 1', status=400 )

        query = models.ChatMessage.objects.filter( invitation = invitation )
        data = []
        for values, obj in zip( query.values(), query ):
            values ['fromUser'] = obj.user.username
            data.append( values )
        return cors_json_response( request, { 'data': data } )
