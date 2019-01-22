from    django.http                 import Http404, HttpResponse
from    django.views                import View
from    .base                       import cors_json_response, get_post_data
from    ..                          import models

import json

from pdb import set_trace as st
import logging


class LearningJournal_V1( View ):

    def get( self, request, resource_id=None, **kwargs ):
        qs = models.LearningJournal.objects.filter( user = request.user )
        if resource_id:
            qs = qs.filter( pk = int( resource_id ) )
        return cors_json_response( request, { 'data': list( qs.values() ) } )


    def post( self, request, resource_id=None, **kwargs ):
        data = get_post_data( request )
        data = json.loads( data ['data'] )

        if not resource_id:
            obj = models.LearningJournal.objects.create(
                user      = request.user,
                title     = data ['title'],
                text      = data ['text'],
                questions = data ['questions'],
            )
            return cors_json_response( request, { 'data': { 'id': obj.id } } )

        try:
            obj = models.LearningJournal.objects.get( pk = int( resource_id ), user = request.user )
        except models.LearningJournal.DoesNotExist:
            return cors_json_response( request, { 'data': '' }, status=400 )

        obj.title     = data ['title']
        obj.text      = data ['text']
        obj.questions = data ['questions']
        obj.save()

        return cors_json_response( request, { 'data': { 'id': obj.id } } )
