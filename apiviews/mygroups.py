from    django.views        import View
from    .base               import cors_json_response

class MyGroups_V1( View ):

    def get( self, request ):
        return cors_json_response(
            request,
            { "data": list( request.user.groups.values() ) }
        )
