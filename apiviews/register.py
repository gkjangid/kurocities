from    django.contrib.auth.models  import User
from    django.core.mail            import EmailMessage
from    django.http                 import Http404
from    django.views                import View
from    random                      import random
from    .base                       import cors_json_response, get_post_data

class Register_V1( View ):

    def post( self, request, **kwargs ):

        data = get_post_data( request )
        try:
            email       = data['email']
            first_name  = data['firstName']
            last_name   = data['lastName']
        except KeyError:
            raise Http404( 'Invalid data' )

        if User.objects.filter( email = email ).count():
            return cors_json_response( request, {
                'error': 'Email already registered',
            })

        password = str( int( random() * 1_000_000 ) )
        user     = User.objects.create_user(
            username    = email,
            email       = email,
            password    = password,
            first_name  = first_name,
            last_name   = last_name,
        )
        self.send_email( request, email, password )
        return cors_json_response( request, {
            'data': data,
        })

    def send_email( self, request, email, password ):
        url = '%s/app/' % request.META ['HTTP_ORIGIN']
        msg = EmailMessage(
            from_email = 'KurioCities<kuriocitiez@gmail.com>',
            to  = [email],
            subject = 'KurioCities Registration',
            body = (
                'You have successfully registered at KurioCities.\n\n'
                'User ID: {email}\n'
                'Password: {password}\n'
                'URL: {url}'
                .format( **locals() )
            ),
        )
        msg.send()
