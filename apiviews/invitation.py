from    django.contrib.auth.models  import Group, User
from    django.core.mail            import EmailMessage
from    django.db                   import transaction
from    django.db.utils             import IntegrityError
from    django.forms.models         import model_to_dict
from    django.http                 import Http404
from    django.utils                import timezone
from    django.views                import View
from    datetime                    import datetime

from    .activity                   import Activity_Get_V1
from    .base                       import cors_json_response, get_post_data, group_access
from    ..                          import models

import  itertools
import  logging


class Invitation_V1( View ):

    def get( self, request, resource_id, **kwargs ):
        if resource_id == '0':
            return self.get_all( request, **kwargs )

        qs = models.Invitation.objects.filter(
            pk=int( resource_id ),
            inviter=request.user,
        )
        if not qs.count():
            raise Http404

        data = qs.values()[0]
        data ['activity'] = model_to_dict( qs[0].activity )
        data ['inviter']  = model_to_dict( qs[0].inviter, exclude=['groups', 'user_permissions'] )
        return cors_json_response( request, { 'data': data } )


    @group_access( ['KCT-Activity-Data'] )
    def get_all( self, request, **kwargs ):
        data = []
        qs = models.Invitation.objects.all()
        for model, invitation in zip( qs, qs.values() ):
            invitation ['activity'] = model_to_dict( model.activity )
            invitation ['inviter']  = model_to_dict( model.inviter, exclude=['groups', 'user_permissions'] )
            data.append( invitation )
        return cors_json_response( request, { 'data': data } )


    @group_access( ['KCT-Checker', 'KCT-Inviter'] )
    def post( self, request, **kwargs ):

        def create_user_activities( users, activity, invitation ):
            errors = []
            for user in users.values():
                ua, created = models.UserActivity.objects.get_or_create(
                    user = user,
                    activity = activity,
                    defaults = { 'invitation': invitation },
                )
                if not created:
                    errors.append( user )
            return errors

        def get_date( data, field ):
            date = data.get( field )
            if not date:
                return
            date = datetime.strptime( date, '%Y-%m-%d' )
            return date

        def get_group_users( groups ):
            users = itertools.chain.from_iterable(
                group.user_set.all()
                for group in Group.objects.filter( name__in=groups )
            )
            users = { user.id: user for user in users }
            return users

        def get_individual_users( individuals ):
            return {
                user.id: user
                for user in User.objects.filter( username__in=individuals )
            }

        def get_users( groups, individuals ):
            group_users      = get_group_users( groups )
            individual_users = get_individual_users( individuals )
            individual_users.update( group_users )
            return individual_users

        def get_object( data, model, param ):
            pk = get_param( data, param )
            try:
                return model.objects.get( pk=pk )
            except model.DoesNotExist:
                msg = 'I2: Invalid %s: %s' % ( param, pk )
                logging.error( msg )
                raise Http404( msg )

        def get_param( data, name ):
            try:
                return data [name]
            except KeyError:
                msg = 'I1: 400: %s' % name
                logging.error( msg )
                raise Http404( msg )

        def send_email_checker( request, activity, invitation ):
            if not activity.checker: return
            origin = request.META ['HTTP_ORIGIN']
            url = '{origin}/ae/#/checker-answers/invitation/{invitation.id}'.format( **locals() )
            title = activity.title.strip()
            msg = EmailMessage(
                from_email = 'KurioCities<kuriocitiez@gmail.com>',
                to  = [activity.checker.email],
                subject = 'Activity Enrollment: %s' % title,
                body = 'You have been assigned as the checker for the "{title}" activity.\n\n{url}'.format(
                    **locals()
                )
            )
            msg.send()


        def send_email_learners( request, activity, users, errors ):
            inviter = request.user
            already_enrolled = [ user.username for user in errors ]
            recipients = [
                user.email for user in users.values()
                if user.email and user.username not in already_enrolled
            ]
            if len( recipients ):
                title = activity.title.strip()
                msg = EmailMessage(
                    from_email = 'KurioCities<kuriocitiez@gmail.com>',
                    to  = [inviter.email],
                    bcc = recipients,
                    subject = 'Activity Enrollment: %s' % title,
                    body = 'You have been enrolled for the "{title}" activity by {inviter.username}.'.format(
                        **locals()
                    )
                )
                logging.warn( 'Emailing to \n%s' % '\n'.join( recipients ) )
                msg.send()
            else:
                logging.error( 'No recipients' )

            return recipients

        # -----

        data        = get_post_data( request )
        groups      = get_param( data, 'groups' )
        individuals = get_param( data, 'individuals' )
        start_date  = get_date( data, 'startDate' )
        deadline    = get_date( data, 'deadline' )
        activity    = get_object( data, models.Activity, 'activityId' )
        users       = get_users( groups=groups, individuals=individuals )
        usernames   = { u.username: None for u in users.values() }
        invitees    = {
            'groups': groups,
            'individuals': individuals,
            'completed':   usernames,
            'checked':     usernames,
        }

        with transaction.atomic():
            invitation  = models.Invitation.objects.create(
                inviter     = request.user,
                activity    = activity,
                invitees    = invitees,
                start_date  = start_date,
                deadline    = deadline,
            )
            errors = create_user_activities(
                    users=users,
                    activity=activity,
                    invitation=invitation,
            )

        send_email_learners( request=request, activity=activity, users=users, errors=errors )
        send_email_checker(  request=request, activity=activity, invitation=invitation )

        return cors_json_response( request, {
            'data': [ user.username for user in errors ]
        })
