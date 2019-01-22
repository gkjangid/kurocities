from    django.db.models            import Q
from    django.forms.models         import model_to_dict
from    django.http                 import Http404
from    django.views                import View

from    .base                       import cors_json_response, group_access
from    ..                          import models


class MessagingActivities_V1( View ):

    @group_access( ['KCT-Messaging', 'KCT-Coach'] )
    def get( self, request, resource_id, **kwargs ):
        data = []
        qs = models.Invitation.objects.filter(
            Q( inviter = request.user ) |
            Q( activity__data__coach = request.user.username ),
        ).order_by( '-created' )

        for model, invitation in zip( qs, qs.values() ):
            invitation ['activity'] = model_to_dict( model.activity )
            invitation ['inviter']  = model_to_dict( model.inviter, exclude=['groups'] )
            data.append( invitation )

        return cors_json_response( request, { 'data': data } )
