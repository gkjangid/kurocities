from    django.views    import View
from    .base           import cors_json_response
from    ..              import models

class UserProfile_V1( View ):

    def get( self, request ):
        try:
            user_profile = models.UserProfile.objects.filter( user = request.user ).values()[0]
        except IndexError:
            models.UserProfile.objects.create( user = request.user )
            user_profile = models.UserProfile.objects.filter( user = request.user ).values()[0]
        return cors_json_response( request, {
            "data": user_profile,
        })
