from    django.http                 import Http404, HttpResponseForbidden
from    django.views                import View
from    .base                       import cors_json_response, get_post_data
from    ..                          import models


class UserActivityToDo_V1( View ):

    def get( self, request, resource_id=None, **kwargs ):
        user_activity_todo_qs = models.UserActivityToDo.objects.filter( user = request.user )

        if resource_id:
            user_activity_todo_qs = user_activity_todo_qs.filter( pk = int( resource_id ) )

        data = []
        for todo, obj in zip( user_activity_todo_qs.values(), user_activity_todo_qs ):
            if obj.user_activity:
                todo ['activity_title'] = obj.user_activity.activity.title
            data.append( todo )

        return cors_json_response( request, {
            "data": data,
            "todoStatuses": models.TODO_STATUSES,
            'actionCategories': self.get_action_categories(),
        })


    def get_action_categories( self ):
        return list( models.Category.objects
            .filter( action_category = True )
            .order_by( 'name' )
            .values()
        )

    def get_category( self, data ):
        obj_id = data.get( 'category_id' )
        if not obj_id:
            return None
        return models.Category.objects.get( pk = obj_id )

    def post( self, request, resource_id, **kwargs ):
        if int( resource_id ) == 0:
            user_activity_todo = models.UserActivityToDo()
        else:
            user_activity_todo = models.UserActivityToDo.objects.get(
                user_activity__user = request.user,
                pk = int( resource_id ),
            )

        data = get_post_data( request )
        user_activity_todo.description = data.get( 'description' )
        user_activity_todo.deadline    = data.get( 'deadline' )
        user_activity_todo.status      = data.get( 'status' )
        user_activity_todo.category    = self.get_category( data )
        user_activity_todo.notes       = data.get( 'notes', '' )
        user_activity_todo.user        = request.user
        user_activity_todo.save()

        return cors_json_response( request, { "id": user_activity_todo.id } )
