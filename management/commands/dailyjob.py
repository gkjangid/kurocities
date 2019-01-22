from    django.core.mail                import send_mass_mail
from    django.core.management.base     import BaseCommand, CommandError
from    kuriocities                     import models
from    collections                     import defaultdict


class Command( BaseCommand ):

    def email_checker( self ):

        def get_check_incomplete( self ):
            recipients = defaultdict( list )
            [
                recipients [invitation.activity.checker.email].append( invitation )
                for invitation in self.check_incomplete_qs
                if invitation.activity.checker.email
            ]
            return {
                recipient : self.get_activities_checks_incomplete( invitations )
                for recipient, invitations in recipients.items()
            }


        incomplete = get_check_incomplete( self )
        mass_mail  = [
            (
                'Incomplete Checks',
                self.get_message_incomplete( incomplete.get( recipient ) ),
                'KurioCities<kuriocitiez@gmail.com>',
                [recipient],
            ) for recipient in incomplete
        ]
        send_mass_mail( mass_mail )


    def email_facilitator( self ):

        def get_check_incomplete( self ):
            recipients = defaultdict( list )
            [
                recipients [invitation.inviter.email].append( invitation )
                for invitation in self.check_incomplete_qs
                if invitation.inviter.email
            ]
            return {
                recipient : self.get_activities_checks_incomplete( invitations )
                for recipient, invitations in recipients.items()
            }


        def get_expired( self ):
            recipients = defaultdict( list )
            [
                recipients [invitation.inviter.email].append( invitation )
                for invitation in self.expired_invitations_qs
                if invitation.inviter.email
            ]
            return {
                recipient : self.get_activities_expired( invitations )
                for recipient, invitations in recipients.items()
            }


        expired         = get_expired( self )
        incomplete      = get_check_incomplete( self )
        all_recipients  = set( expired ) | set( incomplete )
        mass_mail       = [
            (
                'Expired Invitations & Incomplete Checks',
                '%s\n%s' % (
                    self.get_message_expired( expired.get( recipient ) ),
                    self.get_message_incomplete( incomplete.get( recipient ) ),
                ),
                'KurioCities<kuriocitiez@gmail.com>',
                [recipient],
            ) for recipient in all_recipients
        ]
        send_mass_mail( mass_mail )


    def format_date( self, date ):
        if not date:
            return 'N/A'
        return date.strftime( '%d-%b-%Y' )


    def get_message_expired( self, activities ):
        return 'Expired Invitations:\n%s\n' % ( activities or 'N/A' )


    def get_message_incomplete( self, activities ):
        return 'Incomplete Checks\n%s\n' % ( activities or 'N/A' )


    def get_activities_expired( self, invitations ):
        return '\n'.join(
            '- %s (deadline: %s)' % ( invitation.activity.title, self.format_date( invitation.deadline ) )
            for invitation in invitations
        )


    def get_activities_checks_incomplete( self, invitations ):
        return '\n'.join(
            '- %s (completed: %s)' % ( invitation.activity.title, self.format_date( invitation.date_completed ) )
            for invitation in invitations
        )


    def handle( self, *args, **kwargs ):
        self.expired_invitations_qs = models.Invitation.objects.get_expired()
        self.check_incomplete_qs    = models.Invitation.objects.get_check_incomplete()
        self.email_facilitator()
        self.email_checker()
