from channels.generic.websocket import AsyncJsonWebsocketConsumer
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

    async def get_model_is_allowed(self, model_instance):
        return getattr(model_instance, settings.MSOCKS_ALLOW_PARAMETER, False)

    async def connect(self):
        # Assert user is logged in
        if not self.scope['user'].is_authenticated:
            return await self.close()
        self.signal_group_name = await self.get_signal_group_name()

        app = await self.get_app_name()
        model = await self.get_model_name()

        try:
            model_instance = apps.get_model(app, model)
        except LookupError:
            # App or model don't exist
            return await self.close()

        model_is_allowed = await self.get_model_is_allowed(model_instance)
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

    async def get_model_is_allowed(self, model_instance):
        """Self subscriptions ignore model settings"""
        return settings.MSOCKS_ALLOW_SELF_SUBSCRIPTION

    async def get_app_name(self):
        return settings.MSOCKS_SELF_APP

    async def get_model_name(self):
        return settings.MSOCKS_SELF_MODEL

    async def get_signal_group_name(self):
        app = await self.get_app_name()
        model = await self.get_model_name()
        signal = await self.get_signal_type()
        # Keep this user here, because it is used during the eval
        user = self.scope['user']
        relation_id = user.id
        relation_id = eval(settings.MSOCK_AUTH_USER_RELATION_ID)
        return f'sub_{app}_{model}_{relation_id}_{signal}'
