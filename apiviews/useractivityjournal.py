from    django.conf                 import settings
from    django.http                 import Http404, HttpResponse
from    django.forms.models         import model_to_dict
from    django.views                import View
from    .base                       import cors_json_response, get_post_data
from    ..                          import models
import os
import time

from pdb import set_trace as st
import logging


class UserActivityJournal_V1( View ):

    def get( self, request, resource_id=None, **kwargs ):
        if not resource_id:
            qs = models.UserActivityJournal.objects.filter(
                user_activity__user = request.user
            )
            data = []
            for journal, obj in zip( qs.values(), qs ):
                journal ['title']         = obj.user_activity.activity.title
                journal ['user_activity'] = model_to_dict( obj.user_activity )
                journal ['activity']      = model_to_dict( obj.user_activity.activity )
                data.append( journal )
            return cors_json_response( request, { 'data': data } )

        user_activity_id = int( resource_id )
        try:
            user_activity = models.UserActivity.objects.get( pk = user_activity_id )
        except models.UserActivity.DoesNotExist:
            raise Http404( 400 )

        if request.user != user_activity.user:
            return HttpResponse( status=403 )

        qs    = models.UserActivityJournal.objects.filter( user_activity_id = int( resource_id ) )
        count = qs.count()
        if count:
            data = qs.values()[0]
        else:
            data = { 'text': '' }

        return cors_json_response( request, { 'data': data } )


    def post( self, request, resource_id, **kwargs ):
        data = get_post_data( request ) ['data']

        user_activity = models.UserActivity.objects.get( pk = int( resource_id ) )
        if request.user != user_activity.user:
            return HttpResponse( status=403 )

        if hasattr( user_activity, 'useractivityjournal' ):
            user_activity_journal = user_activity.useractivityjournal
        else:
            user_activity_journal = models.UserActivityJournal.objects.create( user_activity = user_activity )

        user_activity_journal.text = data
        user_activity_journal.save()
        return cors_json_response( request, {
            'UserActivityJournalId': user_activity_journal.id,
        })
