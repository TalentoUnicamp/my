from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.auth import get_user
from model_sockets.consumers import ModelSignalConsumer
from channels.db import database_sync_to_async
from .models import Ticket


class TicketSignalConsumer(ModelSignalConsumer):

    async def get_creator_unique_id(self):
        return self.scope['url_route']['kwargs']['unique_id']

    async def get_app_model(self):
        return Ticket

    @database_sync_to_async
    def get_user_is_allowed(self, user):
        # Change it later to only allow mentors and
        # users that can submit tickets
        return user.is_authenticated

    async def get_model_is_allowed(self, model_class):
        return True

    async def get_signal_group_name(self):
        unique_id = await self.get_creator_unique_id()
        signal = await self.get_signal_type()
        return f'ticket_sub_{unique_id}_{signal}'


class OnlineMentorConsumer(AsyncJsonWebsocketConsumer):
    """Consumer that tracks online mentors"""

    group_name = 'online_mentors'

    @database_sync_to_async
    def get_profile(self, user):
        return user.profile

    @database_sync_to_async
    def is_mentor(self, profile):
        return profile.is_mentor

    @database_sync_to_async
    def get_mentor(self, profile):
        return profile.mentor

    @database_sync_to_async
    def set_online(self, mentor):
        mentor.set_online()

    @database_sync_to_async
    def set_offline(self, mentor):
        mentor.set_offline()

    async def connect(self):
        """Someone tried to connect.
        assert they are mentors and, if are, update
        their status and send the list of mentors online
        """

        user = await get_user(self.scope)
        # Don't accept unauthenticated users
        if not user.is_authenticated:
            return await self.close()
        # Reject non mentors
        profile = await self.get_profile(user)
        if not await self.is_mentor(profile):
            return await self.close()

        mentor = await self.get_mentor(profile)
        # Set as online
        await self.set_online(mentor)

        # Subscribe to group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Unsubscribe from group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        user = await get_user(self.scope)
        profile = await self.get_profile(user)
        mentor = await self.get_mentor(profile)
        await self.set_offline(mentor)
