from django.apps import AppConfig
import analytics
from django.conf import settings

class SegmentappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'segmentApp'

    # def ready(self):
    #     analytics.write_key = settings.SEGMENT_SERVER_KEY