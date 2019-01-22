from    django.contrib.auth.models  import User
from    django.db.models            import Q
from    django.http                 import Http404, HttpResponse
from    django.views                import View

from    project                     import settings
from    ..                          import models
from    .base                       import (
    group_access,
    cors_json_response,
    get_post_data,
    get_basic_activity_info,
)

from    pdb import set_trace as st

import  json
import  logging
import  os


class Activity_Get_V1( View ):

    def get( self, request, resource_id=None, **kwargs ):
        if not resource_id:
            return self.getlist( request, **kwargs )
        data = models.Activity.objects.filter( pk=int( resource_id ) ).values()[0]
        return cors_json_response( request, { 'data': data } )

    def getlist_data( self, request, order=None, queryset=None, **kwargs ):
        if queryset is None:
            order    = order or request.GET.get( 'order', 'title' )
            queryset = models.Activity.objects.order_by( order )
            if not request.user.is_superuser:
                groups = [ g.name for g in request.user.groups.all() ]
                queryset = queryset.filter(
                    Q( data__username = request.user.username )
                    | Q( data__editors__in = groups )
                )
        return get_basic_activity_info( queryset )

    def getlist( self, request, **kwargs ):
        return cors_json_response( request, { 'data': self.getlist_data( request ) } )


class Activity_Post_V1( View ):

    def chk_activity_access( self, user, activity ) -> None:
        if user.username == activity.data ['username']:
            return

        if user.is_superuser:
            return

        groups  = [ group.name for group in user.groups.all() ]
        editors = activity.data.get( 'editors' )
        if editors and editors in groups:
            return
        if 'KCT-previewer' in groups:
            return

        raise Http404( 'Invalid user' )


    @group_access( 'KCT-Creator' )
    def post( self, request,  *args, **kwargs ):
        data = json.loads( get_post_data( request )['activity'] )

        if data ['status'] != 'Draft':
            return HttpResponse( 'Invalid activity status', status=403 )

        pk = data['id']
        if pk:
            activity = models.Activity.objects.get( pk=pk )
            self.chk_activity_access( request.user, activity )
        else:
            activity = models.Activity()

        self.save_files( activity, request.FILES )

        activity.title = data['title']
        activity.data  = data
        activity = self.get_user_data   ( request, activity )
        activity = self.get_checker_data( request, activity )
        activity.save()
        activity.data ['id'] = activity.id
        activity.save()
        return cors_json_response( request, { 'data': { "id": activity.id } } )

    def get_checker_data( self, request, activity ):
        checker_questions = [ question.get( 'needsChecker' ) for question in activity.data ['questions'] ]
        if any( checker_questions ):
            checker = (
                activity.data.get( 'coach' )
                if   activity.data.get( 'needsCoach' )
                else activity.data.get( 'checker' )
            )
            if checker:
               activity.checker = User.objects.get( username = checker )
            else:
               activity.checker = request.user
               activity.data ['checker'] = request.user.username
        else:
               activity.checker = None
               activity.data ['checker'] = None

        return activity

    def get_path( self, path ):
        dir_path = os.path.join( settings.MEDIA_ROOT, path )
        os.makedirs( dir_path, exist_ok=True )
        return dir_path

    def get_user_data( self, request, activity ):
        if not activity.created_by_id:
            activity.created_by = request.user
        activity.modified_by = request.user
        return activity

    def save_files( self, activity, files ):
        path = self.get_path( 'Activity/%s' % activity.pk )
        for name, file in files.items():
            name = name.replace( ' ', '-' )
            filename = os.path.join( path, name )
            with open( filename, 'wb' ) as f:
                for chunk in file.chunks():
                    f.write( chunk )
            logging.warn( 'Upload: %s' % filename )


class Activity_V1( View ):

    def get( self, request, *args, **kwargs ):
        return Activity_Get_V1().get( request, *args, **kwargs )

    def post( self, request, *args, **kwargs ):
        try:
            return Activity_Post_V1().post( request, *args, **kwargs )
        except Exception as e:
            error = repr( e )
            logging.error ( error )
            return cors_json_response( request, { 'data': error } )
