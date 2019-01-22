from    django.views        import View
from    .base               import cors_json_response, get_basic_activity_info
from    ..                  import models

class ActivityQuery_V1( View ):

    def get_user_groups( self, request ):
        return [ group.name for group in request.user.groups.all() ]

    def get( self, request, query_type=None, *args, **kwargs ):
        user_groups = self.get_user_groups( request )
        qs = [
            activity for activity in models.Activity.objects.all()
            if self.can_access( request, activity, user_groups )
        ]
        data = get_basic_activity_info( qs )
        return cors_json_response( request, { 'data': data } )

    def can_access( self, request, activity, user_groups ):

        if activity.data.get( 'status' ) != 'Published':
            return 'KCT-Previewer' in user_groups
        else:
            if request.user.is_superuser:
                return True

            if not activity.data.get( 'private' ):
                return True

            private_group = activity.data.get( 'privateGroup' )
            if not private_group:
                return activity.created_by == request.user

            share_groups = activity.data.get( 'shareGroups', [] )
            if private_group:
                share_groups.append( private_group )
            common_groups = set( share_groups ) & set( user_groups )
            return len( common_groups ) > 0

