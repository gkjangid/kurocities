from django.apps import AppConfig


class KuriocitiesConfig(AppConfig):
    name = 'kuriocities'
    verbose_name = 'KurioCities'

    def ready( self ):
        import kuriocities.signals
