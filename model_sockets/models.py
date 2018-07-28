from django.conf import settings
from django.apps import apps
from .subscriptions import generics
from django.db.models.signals import post_save, post_delete, m2m_changed


def load_subscriptions():
    if settings.MSOCKS_ALLOW_SELF_SUBSCRIPTION:
        self_model = apps.get_model(settings.MSOCKS_SELF_APP, settings.MSOCKS_SELF_MODEL)
        selfupdate = generics.SelfUserUpdateReceiver(post_save, 'update')
        selfupdate.register(self_model)

    for event in settings.MSOCKS_MODEL_EVENTS:
        mapper = {
            'create': (generics.CreateReceiver, post_save),
            'update': (generics.UpdateReceiver, post_save),
            'delete': (generics.DeleteReceiver, post_delete),
            'm2m_add': (generics.M2MAddReceiver, m2m_changed),
            'm2m_remove': (generics.M2MRemoveReceiver, m2m_changed),
            'm2m_clear': (generics.M2MClearReceiver, m2m_changed),
        }
        if event in mapper.keys():
            reg = mapper[event][0](mapper[event][1], event)
            reg.register()
