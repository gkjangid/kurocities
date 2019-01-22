from    django.views                import View
from    ..                          import models
from    .base                       import cors_json_response, get_post_data
from    datetime                    import datetime
import  json

class LearningJournalActivity_V1( View ):

    def post( self, request, resource_id, **kwargs ):

        try:
            learning_journal = models.LearningJournal.objects.get( pk = int( resource_id ) )
        except models.LearningJournal.DoesNotExist:
            return cors_json_response( 'LJA1:', status = 400 )
        if learning_journal.user != request.user:
            return cors_json_response( 'LJA2:', status = 403 )

        data          = json.loads( get_post_data( request ) ['data'] )
        activity      = self.save_activity( request, data, learning_journal )
        user_activity = self.save_user_activity( request, activity )
        return cors_json_response( request, { 'data': {
            "activity_id": activity.id,
            "title":       activity.title,
        }})


    def get_checker_data( self, request, activity ):
        activity.checker = None
        activity.data ['checker'] = None
        return activity

    def get_title( self, request, data ):
        username = request.user.username
        time     = datetime.now().strftime( '%Y-%b-%d %H:%M:%S' )
        title    = data ['title']
        return f'{ username } :: { time } :: { title }'

    def get_user_data( self, request, activity ):
        activity.created_by  = request.user
        activity.modified_by = request.user
        return activity

    def save_activity( self, request, data, learning_journal ):
        activity = models.Activity()
        activity.title = self.get_title( request, data )
        activity.data  = data
        activity = self.get_user_data   ( request, activity )
        activity = self.get_checker_data( request, activity )
        activity.learning_journal = learning_journal
        activity.save()
        activity.data ['id'] = activity.id
        activity.save()
        return activity

    def save_user_activity( self, request, activity ):
        return models.UserActivity.objects.create(
            user=request.user,
            activity=activity,
        )
