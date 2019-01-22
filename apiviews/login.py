from django.contrib.auth            import authenticate, login, logout
from django.http                    import Http404
from django.utils.decorators        import method_decorator
from django.views                   import View
from django.views.decorators.csrf   import csrf_exempt, ensure_csrf_cookie
from .base                          import cors_json_response, get_post_data
from ..                             import models


@method_decorator( ensure_csrf_cookie, name='dispatch' )
@method_decorator( csrf_exempt,        name='dispatch' )
class Login_V1( View ):

    def post( self, request, *args, **kwargs ):
        data     = get_post_data( request )
        password = data['password']

        if not password.strip():
            logout( request )
            return cors_json_response( request, {})

        user = authenticate( request=request, username=data['username'], password=password )
        if user is None:
            raise Http404( '401' )
        if not user.is_active:
            raise Http404( '401: Inactive' )
        login( request, user )
        models.UserProfile.objects.get_or_create( user=user, defaults={ 'change_password': True } )
        return cors_json_response( request, {
            "userId":           user.pk,
            "userName":         user.username,
            "email":            user.email,
            "fullName":         user.get_full_name(),
            "groups":           [ group.name for group in user.groups.all() ],
            'change_password':  user.userprofile.change_password,
        })
