from    django.core.mail    import EmailMessage
from    django.http         import Http404
from    django.views        import View
from    django.utils        import timezone
from    .base               import (
    group_access,
    cors_json_response,
    get_post_data,
)
from    .. import models

import  logging


class FacilitatorFeedback_V1( View ):

    @group_access( 'KCT-Inviter' )
    def post( self, request, **kwargs ):

        updated = 0
        for item in get_post_data( request ):
            user_activity = models.UserActivity.objects.get( pk = item ['userActivityId'] )
            if user_activity.comment != item ['comment']:
                user_activity.comment = item ['comment']
                user_activity.date_commented = timezone.now()
                user_activity.save()
                updated =+ 1

        return cors_json_response( request, { 'data': { 'updated': updated } } )
