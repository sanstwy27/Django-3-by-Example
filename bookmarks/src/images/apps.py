from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self):
        # Import Signal Method
        import images.signals