from django.shortcuts import reverse
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from .models import Settings
import json


class SettingsContextMixin(ContextMixin):
    """Settings Context

    Inherit this mixin to automatically get the event settings
    """

    def get_context_data(self, **kwargs):
        settings = Settings.get()
        settings_context = {
            'max_hackers': settings.max_hackers,
            'default_hacker': Settings.default_hacker(settings=settings),
            'default_staff': Settings.default_staff(settings=settings),
            'auto_admit_hackers': Settings.auto_admit_hackers(settings=settings),
            'verify_email': settings.verify_email,
            'registration_opened': Settings.registration_opened(settings=settings),
            'registration_is_open': Settings.registration_is_open(settings=settings),
            'can_confirm': Settings.can_confirm(settings=settings),
            'is_full': Settings.is_full(settings=settings),
            'hackathon_is_happening': Settings.hackathon_is_happening(settings=settings),
            'hackathon_ended': Settings.hackathon_ended(settings=settings),
            'registration_open_seconds': Settings.registration_open_seconds(settings=settings),
            'registration_close_seconds': Settings.registration_close_seconds(settings=settings),
            'confirmation_seconds': Settings.confirmation_seconds(settings=settings),
            'hackathon_start_seconds': Settings.hackathon_start_seconds(settings=settings),
            'hackathon_end_seconds': Settings.hackathon_end_seconds(settings=settings),
            'ticket_expire': settings.ticket_expire,
            'ticket_queue_open': settings.ticket_queue_open,
            'api': {
                'dashboard': reverse('dashboard:index'),
            }
        }
        context = super().get_context_data(**kwargs)
        context['settings_context'] = json.dumps(settings_context)
        return context


class RegistrationOpenMixin(AccessMixin):
    """Only allow if registrations are open"""
    permission_denied_message = 'Estamos fora do período de registro :('

    def dispatch(self, request, *args, **kwargs):
        if not Settings.registration_is_open():
            messages.add_message(self.request, messages.INFO, self.get_permission_denied_message())
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class EventIsHappeningMixin(AccessMixin):
    permission_denied_message = 'O evento não está acontecendo!'

    def dispatch(self, request, *args, **kwargs):
        if not Settings.hackathon_is_happening():
            messages.add_message(self.request, messages.INFO, self.get_permission_denied_message())
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CanConfirmMixin(AccessMixin):
    permission_denied_message = 'Período de confirmação acabou!'

    def dispatch(self, request, *args, **kwargs):
        if not Settings.can_confirm():
            messages.add_message(self.request, messages.INFO, self.get_permission_denied_message())
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
