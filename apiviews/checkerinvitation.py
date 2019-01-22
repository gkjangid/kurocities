from    django.forms.models         import model_to_dict
from    django.http                 import Http404
from    django.views                import View
from    .base                       import cors_json_response, group_access
from    ..                          import models


class CheckerInvitation_V1( View ):

    @group_access( 'KCT-Checker' )
    def get( self, request, resource_id=None, **kwargs ):
        queryset = ( models.Invitation.objects
            .filter(
                date_checked__isnull = True,
                activity__checker = request.user,
            )
            .select_related( 'activity', 'inviter' )
            .order_by( 'date_completed' )
        )
        if resource_id:
            queryset = queryset.filter( pk = resource_id )

        data = []
        for invitation, inv in zip( queryset.values(), queryset ):
            invitation ['activity'] = model_to_dict( inv.activity )
            invitation ['inviter']  = model_to_dict( inv.inviter )
            if 'groups' in invitation ['inviter']:
                del invitation ['inviter'] ['groups']
            data.append( invitation )

        if resource_id:
            data = data [0]

        return cors_json_response( request, { 'data': data } )

