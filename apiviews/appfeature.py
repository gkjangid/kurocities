from    django.http                 import Http404
from    django.views                import View
from    .base                       import cors_json_response
from    ..                          import models


class AppFeature_V1( View ):

    def get( self, request, resource_id=None, **kwargs ):
        queryset = ( models.AppFeature.objects ).all()
        if resource_id:
            queryset = queryset.filter( name = resource_id )

        data = list( queryset.values() )

        if resource_id:
            data = data [0]

        return cors_json_response( request, { 'data': data } )
