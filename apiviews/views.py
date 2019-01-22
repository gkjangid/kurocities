from    django.http         import Http404
from    django.shortcuts    import render
from    django.views        import View
from    importlib           import import_module

from    .base               import cors_json_response
from    ..                  import models
from    .login              import Login_V1


from    pdb import set_trace as st

class InvalidCustomApiError( Exception ):
    pass

class Api( View ):

    def get( self, request, **kwargs ):
        return self.handler( request, 'get', **kwargs )

    def post( self, request, **kwargs ):
        return self.handler( request, 'post', **kwargs )

    def handler( self, request, method, **kwargs ):
        resource = kwargs.get( 'resource' )
        version  = kwargs.get( 'version'  )

        try:
            return self.custom_resource( request, method, **kwargs )
        except InvalidCustomApiError:
            pass

        try:
            api = globals() [ 'ModelView_V%s' % version ]
        except KeyError:
            raise Http404( 'E1: Invalid API version: %s' % version )
        try:
            cls_method = getattr( api(), method )
        except AttributeError:
            raise Http404( 'E2: 405' )
        return cls_method( request, **kwargs )

    def custom_resource( self, request, method, resource, version, **kwargs ):
        try:
            module = import_module( 'kuriocities.apiviews.%s' % resource.lower() )
            resource_api = getattr( module, '%s_V%s' % ( resource, version ), None )
            if not resource_api: raise ImportError
        except ImportError:
            raise InvalidCustomApiError

        try:
            resource_method = getattr( resource_api(), method )
        except AttributeError:
            raise Http404( 'E3: 405' )
        return resource_method( request, **kwargs )


class ModelView_V1( View ):

    def get( self, request, **kwargs ):
        resource_name = self.get_param( kwargs, 'resource' )
        resource_id   = kwargs.get( 'resource_id' )
        data = {
            'data': self.get_model_data( resource_name, resource_id ),
        }
        return cors_json_response( request, data )

    def get_model( self, resource_name ):
        try:
            return getattr( models, resource_name )
        except AttributeError:
            raise Http404( 'MV1: Invalid resource: %s' % resource_name )

    def get_model_data( self, resource_name, resource_id ):
        model    = self.get_model( resource_name )
        queryset = model.objects.all()
        if resource_id:
            queryset = queryset.filter( pk=resource_id )
            try:
                return list( queryset.values() ) [0]
            except IndexError:
                raise Http404( 'MV2: Invalid resource: %s/%s' % ( resource_name, resource_id ) )
        else:
            return list( queryset.values() )

    def get_param( self, kwargs, param ):
        try:
            return kwargs [ 'resource' ]
        except KeyError:
            raise Http404( 'MV3: Invalid API call.' )
