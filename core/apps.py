from importlib import import_module

from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def import_models(self):
        super().import_models()
        self.models_module = import_module(
            f'{self.name}.implementation.services.models'
        )
