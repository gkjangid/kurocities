from    django.contrib.auth.models  import User
from    django.db.utils             import IntegrityError
from    django.http                 import Http404, HttpResponseForbidden
from    django.utils                import timezone
from    django.views                import View
from    .activity                   import Activity_Get_V1
from    .base                       import cors_json_response, get_post_data
from    ..                          import models
import  logging

from    pdb import set_trace as st


class UserActivity_V1( View ):

    def delete( self, request, resource_id ):
        qs = models.UserActivity.objects.filter( pk=resource_id )
        if not qs.count():
            raise Http404
        user_activity = qs.values()[0]
        if qs [0].user != request.user:
            return HttpResponseForbidden
        if user_activity.get( 'state' ) == models.UserActivityState.get_or_create_completed():
            raise Http404( 'Cannot delete activity that is completed' )
        user_activity.pop( 'id' )
        models.UserActivityArchive.objects.create( **user_activity )
        qs.delete()
        return cors_json_response( request, { 'data': resource_id } )

    def get_list( self, request ):
        user_activities = {
            x.activity.pk: x
            for x in models.UserActivity.objects.filter( user=request.user)
        }
        pks             = list( user_activities.keys() )
        queryset        = models.Activity.objects.filter( pk__in = pks ).order_by( '-modified' )
        data            = Activity_Get_V1().getlist_data( request, queryset=queryset )
        for activity in data:
            user_activity               = user_activities[ activity['pk'] ]
            activity['state']           = user_activity.state.name
            activity['deadline']        = user_activity.invitation.deadline   if user_activity.invitation else None
            activity['start_date']      = user_activity.invitation.start_date if user_activity.invitation else None
            activity['journal_count']   = int( hasattr( user_activity, 'useractivityjournal' ) )
        return cors_json_response( request, { "data": data } )

    def get_one( self, request, resource_id ):

        def get_date( date ):
            return timezone.localtime( date ) if date else None

        user_activity_qs = models.UserActivity.objects.filter(
            user         = request.user,
            activity__pk = resource_id,
        )

        user_activity = user_activity_qs.values()[0]
        user_activity[ 'activity' ] = models.Activity.objects.filter(
            pk = user_activity[ 'activity_id' ]
        ).values()[0]

        if user_activity ['invitation_id']:
            invitation = user_activity_qs[0].invitation
            user_activity ['start_date'] = get_date( invitation.start_date )
            user_activity ['deadline']   = get_date( invitation.deadline )

        return cors_json_response( request, {
            "data": user_activity,
        })

    def get( self, request, resource_id=None, **kwargs ):
        if resource_id is None:
            return self.get_list( request )
        else:
            return self.get_one( request, resource_id )

    def post( self, request, resource_id=None, **kwargs ):

        def get_param( data, name ):
            try:
                return data [name]
            except KeyError:
                raise Http404( 'UA1: 400: %s' % name )

        def get_object( data, model, param ):
            pk = get_param( data, param )
            try:
                return model.objects.get( pk=pk )
            except model.DoesNotExist:
                raise Http404( 'UA2: Invalid %s: %s' % ( param, pk ) )

        # -----

        if resource_id:
            return self.delete( request, resource_id )

        data        = get_post_data( request )
        user        = get_object( data, User, 'user' )
        activity    = get_object( data, models.Activity, 'activity' )
        if (
            activity.data ['status'] != 'Published'
            and not request.user.groups.filter( name='KCT-Previewer' ).count()
        ):
            raise Http404( 'UA3: Invalid activity status' )

        try:
            db = models.UserActivity.objects.create(
                user=user,
                activity=activity,
            )
            enrolled = 1
        except IntegrityError as e:
            enrolled = 0

        except Exception as e:
            logging.warn( Exception )
            raise Http404( str(e) )

        return cors_json_response( request, { 'data': { 'enrolled': enrolled } })
