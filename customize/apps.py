from django.apps import AppConfig


class CustomizeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customize"

    def ready(self):
        import customize.signals