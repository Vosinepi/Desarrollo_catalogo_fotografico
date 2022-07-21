from django.apps import AppConfig


class CatalogoFotosAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalogo_fotos_app"

    def ready(self):
        import catalogo_fotos_app.signals
