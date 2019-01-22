from django.views   import View
from .base          import cors_json_response, get_post_data, group_access
from ..             import models

class ActivityTitle_V1( View ):

    @group_access( 'KCT-Creator' )
    def post( self, request, *args, **kwargs ):
        data = get_post_data( request )
        try:
            models.Activity.objects.get_by_natural_key( data )
        except models.Activity.DoesNotExist:
            return cors_json_response( request, { 'data': False } )
        return cors_json_response( request, { 'data': True } )
