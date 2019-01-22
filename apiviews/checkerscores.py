from    django.core.mail    import EmailMessage
from    django.http         import Http404
from    django.views        import View
from    django.utils        import timezone
from    .base               import (
    group_access,
    cors_json_response,
    get_post_data,
    calculate_total_scores,
    update_user_profile,
)
from    .. import models

import  logging


class CheckerScores_V1( View ):

    def is_check_completed( self, user_activity, question_scores ):
        needs_checker   = user_activity.activity.needs_checker
        questions       = user_activity.activity.data ['questions']

        checker = 0
        for questionIdx, question in enumerate( questions ):
            if not needs_checker( question ): continue
            checker  += 1
            score     = question_scores [ str( questionIdx ) ]
            qscore    = score [0]
            max_score = score [1]
            if not qscore:
                return False
        else:
            if checker:
                return True
            else:
                return False


    @group_access( 'KCT-Checker' )
    def post( self, request, **kwargs ):
        data = get_post_data( request ).get( 'data' )
        if not data:
            raise Http404( 'CS1:' )

        for ua_score in data:
            user_activity = ( models.UserActivity.objects
                .select_related( 'activity' )
                .get( pk=ua_score ['user_activity'] )
            )

            if ua_score ['score']:
                self.update_user_activity( request, user_activity, ua_score )
                update_user_profile( request.user )

        return cors_json_response( request, { 'data': user_activity.scores } )


    def send_activity_checked_email( self, request, user_activity ):
        origin = request.META ['HTTP_ORIGIN']
        email = user_activity.invitation.inviter.email
        url = '%s/ae/#/facilitator-activity/%s' % ( origin, user_activity.invitation.id )

        if not email:
            logging.error( 'No email address found for User-Activity: %s' % user_activity.id )
            return

        recipients = [ email ]
        title = user_activity.activity.title.strip()
        msg = EmailMessage(
            from_email = 'KurioCities<kuriocitiez@gmail.com>',
            to  = recipients,
            subject = 'Activity Checked: %s' % title,
            body = url,
        )
        logging.warn( 'Emailing to %s' % email )
        msg.send()


    def update_user_activity( self, request, user_activity, ua_score ):
        score           = ua_score ['score']
        max_score       = ua_score ['max_score']
        questionIdx     = ua_score ['questionIdx']
        question_scores = user_activity.scores ['questions']
        question_scores [ str( questionIdx ) ] = [ score, max_score ]
        user_activity.scores = calculate_total_scores(
            user_activity.activity.data ['questions'],
            user_activity.scores,
        )
        date_time = ( timezone.now()
            if self.is_check_completed( user_activity, question_scores )
            else None
        )
        if date_time:
            if not user_activity.date_checked:
                user_activity.date_checked = date_time
            self.update_invitation( request, user_activity, date_time )

        user_activity.save()


    def update_invitation( self, request, user_activity, date_time ):
        invitation = user_activity.invitation
        if invitation:
            username  = user_activity.user.username
            usernames = invitation.invitees.get( 'checked' )
            if username in usernames and not usernames [username]:
                usernames [username] = date_time.isoformat()
                if invitation.checked():
                    invitation.date_checked = date_time
                    self.send_activity_checked_email( request, user_activity )
                invitation.save()
