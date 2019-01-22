from django.core.management.base    import BaseCommand, CommandError
from django.core.mail               import mail_admins


class Command( BaseCommand ):

    def add_arguments( self, parser ):
        parser.add_argument( 'app' )

    def handle( self, *args, app, **kwargs ):

        with open( 'test_%s.log' % app ) as f:
            message = f.read()

        mail_admins(
            subject = 'Test Error: %s' % app,
            message = message,
        )
