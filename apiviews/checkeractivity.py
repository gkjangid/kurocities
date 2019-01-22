from    django.forms.models         import model_to_dict
from    django.http                 import Http404
from    django.views                import View
from    .base                       import cors_json_response, group_access
from    ..                          import models


class CheckerActivity_V1( View ):

    @group_access( 'KCT-Checker' )
    def get( self, request, **kwargs ):
        data = list( models.UserActivity.objects
            .filter(
                activity__checker = request.user,
                date_checked__isnull = True,
                completed__isnull = False,
            )
            .order_by( 'activity__title', 'activity__id' )
            .distinct( 'activity__title', 'activity__id' )
            .values  ( 'activity__title', 'activity__id' )
        )
        return cors_json_response( request, { 'data': data } )
