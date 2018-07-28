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


class M2MAddReceiver(BaseSubscriptionReceiver):

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        action = kwargs['action']
        if action != 'post_add':
            return
        instance = kwargs['instance']
        self.data = self.get_instance_fields(instance.__class__, instance)
        self.dispatch()
        print()

    def is_valid(self):
        if not getattr(self.instance.__class__, settings.MSOCKS_ALLOW_PARAMETER, False):
            # This model does not allow subscriptions
            return False
        return True

    @property
    def group_name(self):
        return f'sub_{self.sender._meta.app_label}_{self.instance.__class__.__name__}{"".join([f"_{arg}" for arg in self.volatile_args])}'


class M2MRemoveReceiver(BaseSubscriptionReceiver):

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        action = kwargs['action']
        if action != 'post_remove':
            return
        instance = kwargs['instance']
        self.data = {
            'id': getattr(instance, 'id', None)
        }
        self.dispatch()
        print()

    def is_valid(self):
        if not getattr(self.instance.__class__, settings.MSOCKS_ALLOW_PARAMETER, False):
            # This model does not allow subscriptions
            return False
        return True

    @property
    def group_name(self):
        return f'sub_{self.sender._meta.app_label}_{self.instance.__class__.__name__}{"".join([f"_{arg}" for arg in self.volatile_args])}'


class M2MClearReceiver(BaseSubscriptionReceiver):

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        action = kwargs['action']
        if action != 'post_clear':
            return
        instance = kwargs['instance']
        self.data = {
            'id': getattr(instance, 'id', None)
        }
        self.dispatch()

    def is_valid(self):
        if not getattr(self.instance.__class__, settings.MSOCKS_ALLOW_PARAMETER, False):
            # This model does not allow subscriptions
            return False
        return True

    @property
    def group_name(self):
        return f'sub_{self.sender._meta.app_label}_{self.instance.__class__.__name__}{"".join([f"_{arg}" for arg in self.volatile_args])}'


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
