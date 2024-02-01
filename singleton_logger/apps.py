from django.apps import AppConfig


class SingletonLoggerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'singleton_logger'
