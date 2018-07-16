from django.shortcuts import reverse
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings
import json


class SidebarContextMixin(LoginRequiredMixin, ContextMixin):
    """Sidebar Context

    Inherit this mixin to automatically get the context required for
    the sidebar
    """

    active_tab = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sidebar_context = {
            'active_tab': self.active_tab,
            'event_name': settings.EVENT_NAME,
            'event_logo': static('project/img/logo.svg'),
            'redirect_urls': {
                'dashboard': reverse('dashboard:index'),
                'application': reverse('application:form'),
                'company': reverse('company:index'),
                'team': reverse('dashboard:index'),
                'admin': reverse('godmode:index'),
                'staff': reverse('staff:index'),
                'logout': reverse('profile:logout'),
            }
        }
        context['sidebar_context'] = json.dumps(sidebar_context)
        return context


class UserContextMixin(ContextMixin):
    """User context mixin

    Inherit this mixin to get user data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        profile = user.profile
        user_context = {
            'is_admin': profile.is_admin,
            'token': profile.token,
            'is_verified': profile.is_verified,
            'unique_id': profile.unique_id,
            'is_hacker': profile.is_hacker,
            'is_staff': profile.is_staff,
            'is_employee': profile.is_employee,
            'state': profile.state,
            'email': user.email,
            'social': {
                'has_facebook': profile.has_facebook,
                'has_github': profile.has_github,
                'has_google': profile.has_google
            }
        }
        context['user_context'] = json.dumps(user_context)
        return context


class LoginContextMixin(ContextMixin):
    """Login context mixin

    Inherit this mixin to get user data
    """

    form_error = ''
    form_success = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        login_context = {
            'event_logo': static('project/img/logo.svg'),
            'event_bg': static('project/img/bg.png'),
            'check_token_url': reverse('profile:api:check_token'),
            'reset_email_url': reverse('profile:api:reset_token_email'),
            'error': self.form_error,
            'success': self.form_success,
            'social_urls': {
                'facebook': reverse('social:login', kwargs={'provider': 'facebook'}),
                'github': reverse('social:login', kwargs={'provider': 'github'}),
                'google': reverse('dashboard:index'),
            }
        }
        context['login_context'] = json.dumps(login_context)
        return context
