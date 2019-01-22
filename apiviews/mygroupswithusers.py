from    django.views        import View
from    .base               import cors_json_response

class MyGroupsWithUsers_V1( View ):

    def get_users( self, group, group_info ):
        group_info ['users'] = list( group.user_set.order_by( 'username' ).values() )
        return group_info

    def get( self, request ):
        groups_qs = ( request.user.groups
            .order_by( 'name' )
        )
        groups = [
            self.get_users( group, group_info )
            for group, group_info in zip( groups_qs, groups_qs.values() )
        ]
        return cors_json_response(
            request,
            { "data": list( groups ) },
        )
