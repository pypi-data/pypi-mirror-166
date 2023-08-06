from django.conf import settings
import analytics
from segmentApp.utils import generate_anonymous_id

def error_handler(error):
    print(f'erro {error}')

class SegmentClient():
    def __init__(self, write_key=settings.SEGMENT_SERVER_KEY, on_error=error_handler, send=True, sync_mode=False, debug=False):
        self.write_key = write_key
        self.on_error = on_error
        self.debug = debug
        self.send = send
        self.sync_mode = sync_mode
        self.client = analytics.Client(self.write_key, on_error=self.on_error, send=self.send, sync_mode=self.sync_mode, debug=self.debug)

    # def identify_anonymous(self, anonymous_id=None):
    #     if anonymous_id is None:
    #         anonymous_id = generate_anonymous_id()
    #     return self.client.identify(anonymous_id)

    def identify_user(self, user):
        return self.client.identify(user.id, {
            'name': user.full_name,
            'email': user.email
        })
        
    def track_anonymous(self,  event_name, anonymous_id=None, properties={}, integrations={}):
        if anonymous_id is None:
            anonymous_id = generate_anonymous_id()
        return self.client.track(anonymous_id=anonymous_id, event=event_name, properties=properties, integrations=integrations)

    def track_user(self, user, event_name, properties={}, integrations={}):
        return self.client.track(user.id, event_name, properties=properties, integrations=integrations)

    def group(self, user, group_id, traits={}):
        return self.client.group(user.id, group_id, traits=traits)