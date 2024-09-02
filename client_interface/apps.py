from django.apps import AppConfig


class ClientInterfaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_interface'

    def ready(self):
        import client_interface.signals
