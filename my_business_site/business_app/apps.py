from django.apps import AppConfig

class BusinessAppConfig(AppConfig):
    name = 'business_app'

    def ready(self):
        # Импорт и регистрация сигналов
        # import my_business_site.business_app.signals
        from . import signals