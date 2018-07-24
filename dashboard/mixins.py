from django.shortcuts import reverse
from django.views.generic.base import ContextMixin
from django.conf import settings
import json


class DashboardContextMixin(ContextMixin):
    """Dasboard context mixin

    Inherit this mixin to get dashboard data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dashboard_context = {
            'event_name': settings.EVENT_NAME,
            'api': {
                'change_token': reverse('profile:api:change_token'),
                'change_email': reverse('profile:api:change_email'),
                'unlink_provider': reverse('social:api:unlink_provider'),
                'confirm': reverse('hacker:api:confirm'),
                'withdraw': reverse('hacker:api:withdraw'),
                'undo_withdraw': reverse('hacker:api:undo_withdraw'),
            },
            'social_urls': {
                'facebook': reverse('social:login', kwargs={'provider': 'facebook'}),
                'github': reverse('social:login', kwargs={'provider': 'github'}),
                'google': reverse('social:login', kwargs={'provider': 'google'}),
            }
        }
        context['dashboard_context'] = json.dumps(dashboard_context)
        return context
