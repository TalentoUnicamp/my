from django.db.models.signals import post_delete
from model_sockets.subscriptions import base


class BaseTicketSubscription(base.BaseSubscriptionReceiver):
    """Allows users and mentors to subscribe to tickets

    Tickets are fetched with relation to a profile
    and only updates of the latest ticket are dispatched
    """

    sub_type = 'publish.subscription'

    def get_group_name(self):
        return f'ticket_sub_{self.instance.creator.unique_id}{"".join([f"_{arg}" for arg in self.volatile_args])}'

    def is_valid(self):
        """Whether or not the update
        is valid. That is, if it is allowed
        """
        if not super().is_valid():
            return False
        # If not deleting
        if self.signal != post_delete:
            # Check if it is the latest ticket
            if self.sender.objects.filter(creator=self.instance.creator).last().id == self.instance.id:
                return True
            return False
        # If deleting, we have to send and the client has to fetch manually
        # the latest instance
        return True


class CreateTicketSubscription(BaseTicketSubscription):

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        # Only accept created signals
        if not kwargs['created']:
            return

        instance = kwargs['instance']
        self.data = self.get_instance_fields(sender, instance)
        self.dispatch()


class UpdateTicketSubscription(BaseTicketSubscription):

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        # Only accept created signals
        if kwargs['created']:
            return
        instance = kwargs['instance']
        self.data = self.get_instance_fields(sender, instance)
        self.dispatch()


class DeleteTicketSubscription(BaseTicketSubscription):

    def receive(self, sender, **kwargs):
        super().receive(sender, **kwargs)
        instance = kwargs['instance']
        self.data = {
            'id': getattr(instance, 'id', None)
        }
        self.dispatch()
