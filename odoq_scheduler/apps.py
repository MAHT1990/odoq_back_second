from django.apps import AppConfig
from django.conf import settings


class OdoqSchedulerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'odoq_scheduler'
    has_started = False

    def ready(self):
        if settings.SCHEDULER_DEFAULT and not self.has_started:
            from utils import schedulers
            schedulers.start_scheduler()
            self.has_started = True


