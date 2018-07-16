from django.conf import settings
from django.apps import apps
from .subscriptions.generics import UpdateReceiver, CreateReceiver, DeleteReceiver, SelfUserUpdateReceiver
from django.db.models.signals import post_save, post_delete


def load_subscriptions():
    if settings.MSOCKS_ALLOW_SELF_SUBSCRIPTION:
        self_model = apps.get_model(settings.MSOCKS_SELF_APP, settings.MSOCKS_SELF_MODEL)
        selfupdate = SelfUserUpdateReceiver(post_save, 'update')
        selfupdate.register(self_model)

    for event in settings.MSOCKS_MODEL_EVENTS:
        mapper = {
            'create': (CreateReceiver, post_save),
            'update': (UpdateReceiver, post_save),
            'delete': (DeleteReceiver, post_delete)
        }
        if event in mapper.keys():
            reg = mapper[event][0](mapper[event][1], event)
            reg.register()
