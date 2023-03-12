from django.apps import AppConfig


class OdoqModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'odoq_models'
    ready_has_run = False

    def ready(self):
        print('odoq_models ready')
        if not self.ready_has_run:
            from utils.schedulers import start_test_scheduler
            start_test_scheduler()
            self.ready_has_run = True