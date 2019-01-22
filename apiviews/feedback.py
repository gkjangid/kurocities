# from    django.contrib.auth.models  import Group, User
from    django.core.mail            import EmailMessage
# from    django.db                   import transaction
# from    django.db.utils             import IntegrityError
# from    django.forms.models         import model_to_dict
# from    django.http                 import Http404
# from    django.utils                import timezone
from    django.views                import View
# from    datetime                    import datetime

from    .base                       import cors_json_response, get_post_data
from    ..                          import models

import  logging
from    pdb import set_trace as st


class Feedback_V1( View ):

    def post( self, request, **kwargs ):
        data         = get_post_data( request )
        feedback     = data ['feedback']
        feedback_obj = models.Feedback.objects.create(
            user     = request.user,
            feedback = feedback,
        )
        recipients = [
            'ricard.gras@edunexis.com',
        ]
        EmailMessage(
            from_email = 'KurioCities<kuriocitiez@gmail.com>',
            to         = [recipients],
            subject    = 'KurioCities Feedback',
            body       = 'User: {request.user.username}\n\n{feedback}'.format( **locals() ),
        ).send()
        return cors_json_response( request, {
            'data': feedback_obj.id
        })
