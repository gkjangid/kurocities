from django.core.mail           import EmailMessage
from django.contrib.auth.models import Group
from django.views               import View
from django.http                import Http404, HttpResponse
from django.utils               import timezone
from .base                      import cors_json_response, get_post_data, group_access
from ..                         import models


class ActivityStatus_V1( View ):

    def chk_private_group_access( self, request, activity ):
        if activity.data.get( 'private' ):
            group  = activity.data.get( 'privateGroup' )
            groups = [ g.name for g in request.user.groups.all() ]
            if group not in groups and not request.user.is_superuser:
                return False
        return True


    @group_access( 'KCT-Reviewer' )
    def chk_status_draft( self, request, data, activity, *args, **kwargs ):
        if activity.data ['status'] != 'Review':
            return HttpResponse( 'Invalid status', status=403 )

        if not self.chk_private_group_access( request, activity ):
            return HttpResponse( 'Invalid user', status=403 )


    @group_access( 'KCT-Reviewer' )
    def chk_status_published( self, request, data, activity, *args, **kwargs ):
        if activity.data ['status'] != 'Review':
            return HttpResponse( 'Invalid status', status=403 )

        if not self.chk_private_group_access( request, activity ):
            return HttpResponse( 'Invalid user', status=403 )


    @group_access( 'KCT-Creator' )
    def chk_status_review( self, request, data, activity, *args, **kwargs ):
        if activity.data ['status'] != 'Draft':
            return HttpResponse( 'Invalid status', status=403 )

        if request.user != activity.created_by and not request.user.is_superuser:
            return HttpResponse( 'Invalid user', status=403 )


    def get_review_history( self, status, activity, data ):
        history  = activity.data.setdefault( 'reviewHistory', [] )
        comment  = data.get( 'reviewComment', '' )
        if status == 'Review':
            comment = 'Submitted for review.'
        elif status == 'Published':
            comment = 'Published. %s' % comment
        elif status == 'Draft':
            comment = 'Rejected: %s' % comment
        history.append({
            'date':     timezone.now().isoformat(),
            'comment':  comment,
        })
        return history


    def get_reviewers( self, activity ):
        reviewers = {
            u.email
            for u in Group.objects.get( name='KCT-Reviewer' ).user_set.all()
            if u.email
        }
        if activity.data ['private']:
            try:    group = Group.objects.get( name = activity.data ['privateGroup'] )
            except  Group.DoesNotExist:
                raise Http404( 'AS1: Invalid private group' )

            private_group_users = { u.email for u in group.user_set.all() if u.email }
            reviewers = reviewers & private_group_users

        return list( reviewers )


    @group_access( ['KCT-Creator', 'KCT-Inviter'] )
    def post( self, request, *args, **kwargs ):
        data        = get_post_data( request )
        activity_id = data.get( 'activityId' )
        status      = data.get( 'status' )
        if not activity_id or not status:
            return HttpResponse( 'Bad request', status=400 )
        try:
            activity = models.Activity.objects.get( pk=activity_id )
        except models.Activity.DoesNotExist:
            return Http404( 'Invalid ID' )

        chk_status = getattr( self, 'chk_status_%s' % status.lower() )
        isvalid = chk_status( request, data, activity )
        if isvalid is not None:
            return isvalid

        reviewers = self.get_reviewers( activity )
        activity.data ['status'] = status
        activity.data ['reviewHistory'] = self.get_review_history( status, activity, data )
        activity.save()
        self.send_email( request=request, data=data, activity=activity, status=status, reviewers=reviewers )
        return cors_json_response( request, { 'status': status } )


    def send_email( self, request, data, activity, status, reviewers ):
        origin   = request.META ['HTTP_ORIGIN']
        url      = '{origin}/ae/#/activity/{activity.id}'
        subject  = 'Activity {status}: {activity.title}'.format( **locals() )
        comment  = data.get( 'reviewComment', 'N/A' )
        template = {
            'Review':    'Activity "{activity.title}" has been submitted for review.\n\n{url}'.format( **locals() ),
            'Draft':     'Activity "{activity.title}" has been rejected during review.\n\n'
                         'Comment:\n{comment}\n\n{url}'.format( **locals() ),
            'Published': 'Activity "{activity.title}" has been published.\n\n{url}'.format( **locals() ),
        }
        body = template [status].format( **locals() )
        if status != 'Review':
            recipient = [activity.created_by.email]
        else:
            recipient = reviewers

        msg = EmailMessage(
            from_email = 'KurioCities<kuriocitiez@gmail.com>',
            to  = recipient,
            subject = subject,
            body = body,
        ).send()


