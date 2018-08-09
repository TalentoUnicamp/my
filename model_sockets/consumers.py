from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.auth import get_user
from django.apps import apps
from django.conf import settings
from . import serializer
import json


class ModelSignalConsumer(AsyncJsonWebsocketConsumer):

    async def get_app_name(self):
        return self.scope['url_route']['kwargs']['app']

    async def get_model_name(self):
        return self.scope['url_route']['kwargs']['model']

    async def get_signal_type(self):
        return self.scope['url_route']['kwargs']['signal']

    async def get_app_model(self):
        app = await self.get_app_name()
        name = await self.get_model_name()
        return apps.get_model(app, name)

    async def get_signal_group_name(self):
        app = await self.get_app_name()
        model = await self.get_model_name()
        signal = await self.get_signal_type()
        return f'sub_{app}_{model}_{signal}'

    async def get_model_is_allowed(self, model_class):
        return getattr(model_class, settings.MSOCKS_ALLOW_PARAMETER, False)

    @database_sync_to_async
    def get_user_is_allowed(self, user):
        return user.is_authenticated

    async def connect(self):
        # Assert user is allowed
        user_is_allowed = await self.get_user_is_allowed(await get_user(self.scope))
        if not user_is_allowed:
            return await self.close()
        self.signal_group_name = await self.get_signal_group_name()

        try:
            model_class = await self.get_app_model()
        except LookupError:
            # App or model don't exist
            return await self.close()

        model_is_allowed = await self.get_model_is_allowed(model_class)
        if not model_is_allowed:
            # This model does not allow subscriptions
            return await self.close()

        # Subscribe to the group
        await self.channel_layer.group_add(
            self.signal_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        signal_group_name = await self.get_signal_group_name()
        # Unsubscribe from group
        await self.channel_layer.group_discard(
            signal_group_name,
            self.channel_name
        )

    async def publish_subscription(self, event):
        data = event['data']
        await self.send_json(content=data)

    @classmethod
    async def encode_json(cls, content):
        return json.dumps(serializer.filter_json(content))


class SelfSignalConsumer(ModelSignalConsumer):
    """Tracks changes on the current authenticated user."""

    async def get_model_is_allowed(self, model_class):
        """Self subscriptions ignore model settings"""
        return settings.MSOCKS_ALLOW_SELF_SUBSCRIPTION

    async def get_app_name(self):
        return settings.MSOCKS_SELF_APP

    async def get_model_name(self):
        return settings.MSOCKS_SELF_MODEL

    @database_sync_to_async
    def get_relation_id(self, user):
        # Keep this user here, because it is used during the eval
        relation_id = user.id
        return eval(settings.MSOCK_AUTH_USER_RELATION_ID)

    async def get_signal_group_name(self):
        app = await self.get_app_name()
        model = await self.get_model_name()
        signal = await self.get_signal_type()
        relation_id = await self.get_relation_id(await get_user(self.scope))
        return f'sub_{app}_{model}_{relation_id}_{signal}'
