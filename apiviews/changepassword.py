from django.views                   import View
from .base                          import cors_json_response, get_post_data


class ChangePassword_V1( View ):

    def post( self, request, *args, **kwargs ):
        data = get_post_data( request )
        new_password = data['newPassword']
        if not request.user.check_password( data['currentPassword'] ):
            return cors_json_response( request, { 'error': 'Invalid current password' } )
        else:
            request.user.set_password( data['newPassword'] )
            request.user.save()
            request.user.userprofile.change_password = False
            request.user.userprofile.save()
            return cors_json_response( request, { 'error': None } )
