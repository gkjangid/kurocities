from    django.views                import View
from    .base                       import cors_json_response, group_access
from    ..                          import models


class InvitationTeams_V1( View ):

    @group_access( ['KCT-Messaging', 'KCT-Coach'] )
    def get( self, request, resource_id, **kwargs ):

        teams = list({
            values [0]
            for values in models.UserActivity.objects.filter(
                    invitation_id = int( resource_id ),
                ).values_list( 'team' )
            if values [0] and values [0].strip()
        })
        return cors_json_response( request, { 'teams': teams } )
