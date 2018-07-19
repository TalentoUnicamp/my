from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.conf import settings
from .. import serializer
from .utils import get_fields_and_properties


# Prevent garbage collector from cleaning the instances
subscribed_instances = []


class BaseSubscriptionReceiver:

    def __init__(self, signal, *args):
        self.args = args
        self.volatile_args = args
        self.signal = signal
        self.all_fields = {}
        self.sender = None

    @property
    def group_name(self):
        return f'sub_{self.sender._meta.app_label}_{self.sender.__name__}{"".join([f"_{arg}" for arg in self.volatile_args])}'

    def get_allowed_fields(self, all_fields={}):
        all_fields = all_fields or self.all_fields
        return getattr(self.sender, settings.MSOCKS_FIELDS_PARAMETER, []) or all_fields.keys()

    def get_allowed_data(self, all_fields={}):
        data = {}
        for field in self.get_allowed_fields(all_fields):
            field_value = field
            if not isinstance(field, str):
                if not isinstance(field, list) and not isinstance(field, tuple):
                    raise TypeError(f'Field {field} should be str, tuple or list. Is {type(field)}')
                if len(field) != 2:
                    raise ValueError(f'Field {field} has {len(field)}. Should have 2')
                field_value = field[1]
                field = field[0]
            obj = eval('self.instance.' + field_value)
            if callable(obj):
                obj = obj()
            data[field] = obj
        return data

    def dispatch(self):
        if not self.is_valid():
            return
        response = {}
        response['data'] = self.get_allowed_data()
        response['type'] = 'publish.subscription'
        response = serializer.filter_json(response)
        async_to_sync(get_channel_layer().group_send)(
            self.group_name,
            response
        )

    def receive(self, sender, **kwargs):
        self.volatile_args = self.args
        self.sender = sender
        self.instance = kwargs['instance']

    def is_valid(self):
        if not getattr(self.sender, settings.MSOCKS_ALLOW_PARAMETER, False):
            # This model does not allow subscriptions
            return False
        return True

    def register(self, sender=None, dispatch_uid=None):
        self.signal.connect(self.receive, sender=sender, dispatch_uid=dispatch_uid)
        subscribed_instances.append(self)

    def unregister(self, sender=None, dispatch_uid=None):
        self.signal.disconnect(sender=sender, dispatch_uid=dispatch_uid)

    def get_instance_fields(self, sender, instance):
        data = get_fields_and_properties(sender, instance)
        return data


class BaseInstanceUpdateReceiver(BaseSubscriptionReceiver):
    """Allows subscription of individual instances.

    like subscriptions of a specific user"""

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        # Only accept updated signals
        if kwargs['created']:
            return
        self.volatile_args = [getattr(self.instance, 'id', None)] + list(self.args)
        self.all_fields = self.get_instance_fields(sender, self.instance)
        self.dispatch()
