from django.conf import settings
from django.apps import AppConfig
from .custom_appconf import NoPrefixAppConf
from .models import load_subscriptions
import os


class ModelSocketsConfig(AppConfig):
    name = 'model_sockets'

    def ready(self):
        load_subscriptions()


class ModelSocketsSettings(NoPrefixAppConf):
    ASGI_APPLICATION = "model_sockets.router_application.application"
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    REDIS_URL_LIST = [REDIS_URL]
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": REDIS_URL_LIST,
            },
        },
    }
    # Parameter that the api looks for inside models
    MSOCKS_ALLOW_PARAMETER = 'msocks_allow'
    # Parameter that the api looks for inside models for valid fields
    MSOCKS_FIELDS_PARAMETER = 'msocks_fields'
    # Name of the app containing the self model
    MSOCKS_SELF_APP = 'auth'
    # Name of the self Model
    MSOCKS_SELF_MODEL = 'User'
    # Relation from an auth User model to the self model
    MSOCK_AUTH_USER_RELATION_ID = 'user.id'
    # Whether or not to allow self subscriptions
    MSOCKS_ALLOW_SELF_SUBSCRIPTION = True
    # Self subscriptions fields
    MSOCKS_SELF_SUBSCRIPTION_FIELDS = ['id', 'first_name', 'email', 'username', 'full_name']
    # Events to subscribe all models to
    MSOCKS_MODEL_EVENTS = ['create', 'update', 'delete', 'm2m_add', 'm2m_remove', 'm2m_clear']
