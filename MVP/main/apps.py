from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    # Signal import when adding a new field to the db
    def ready(self) -> None:
        import main.signals
