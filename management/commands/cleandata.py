from django.core.management.base    import BaseCommand, CommandError
from kuriocities.models             import Activity

class Command( BaseCommand ):

    def handle( self, *args, **kwargs ):

        for activity in Activity.objects.all():
            activity.data['id'] = activity.pk
            if activity.data.get( 'private' ) == None:
                activity.data['private'] = False
            activity.save()
