from django.apps import AppConfig


class ProvidersConfig(AppConfig):
    name = 'providers'

    def ready(self):
        import providers.signals
