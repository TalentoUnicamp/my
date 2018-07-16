from .base import BaseSubscriptionReceiver, BaseInstanceUpdateReceiver
from django.conf import settings


class CreateReceiver(BaseSubscriptionReceiver):

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        # Only accept created signals
        if not kwargs['created']:
            return

        instance = kwargs['instance']
        self.data = self.get_instance_fields(sender, instance)
        self.dispatch()


class UpdateReceiver(BaseSubscriptionReceiver):

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        # Only accept updated signals
        if kwargs['created']:
            return
        instance = kwargs['instance']
        self.data = self.get_instance_fields(sender, instance)
        self.dispatch()


class DeleteReceiver(BaseSubscriptionReceiver):

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        instance = kwargs['instance']
        self.data = {
            'id': getattr(instance, 'id', None)
        }
        self.dispatch()


class SelfUserUpdateReceiver(BaseInstanceUpdateReceiver):

    def get_allowed_fields(self, all_fields={}):
        # Self subscription fields are to be different from
        # regular updates from the same model

        all_fields = all_fields or self.all_fields
        return settings.MSOCKS_SELF_SUBSCRIPTION_FIELDS or all_fields.keys()

    def is_valid(self):
        """Self subscriptions ignore the model's allow field"""
        if not settings.MSOCKS_ALLOW_SELF_SUBSCRIPTION:
            # This model does not allow subscriptions
            return False
        return True
