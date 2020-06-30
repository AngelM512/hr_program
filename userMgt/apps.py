from django.apps import AppConfig


class UsermgtConfig(AppConfig):
    name = 'userMgt'

    def ready(self):
        import userMgt.signals
