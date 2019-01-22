from    django.forms.models         import model_to_dict
from    django.http                 import Http404
from    django.views                import View
from    .base                       import cors_json_response, group_access
from    ..                          import models


class FacilitatorInvitation_V1( View ):

    @group_access( 'KCT-Inviter' )
    def get( self, request, resource_id=None, **kwargs ):
        queryset = ( models.Invitation.objects
            .filter(
                inviter = request.user,
            )
            .select_related( 'activity' )
            .order_by( '-created' )
        )
        if resource_id:
            queryset = queryset.filter( pk = resource_id )

        data = []
        for invitation, inv in zip( queryset.values(), queryset ):
            invitation ['activity'] = model_to_dict( inv.activity )
            data.append( invitation )

        if resource_id:
            data = data [0]

        return cors_json_response( request, { 'data': data } )

