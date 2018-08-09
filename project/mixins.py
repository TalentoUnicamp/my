from django.shortcuts import reverse
from django.views.generic.base import ContextMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings as dj_settings
from rest_framework_csv.renderers import CSVRenderer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework_yaml.renderers import YAMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework_msgpack.renderers import MessagePackRenderer
import json
from .renderers import NotNestedCSVRenderer, TSVRenderer, NotNestedTSVRenderer
from settings.mixins import SettingsContextMixin


class SidebarContextMixin(LoginRequiredMixin, SettingsContextMixin, ContextMixin):
    """Sidebar Context

    Inherit this mixin to automatically get the context required for
    the sidebar
    """

    active_tab = ''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sidebar_context = {
            'active_tab': self.active_tab,
            'event_name': dj_settings.EVENT_NAME,
            'event_logo': static('project/img/logo.svg'),
            'event_logo_png': static('project/img/logo.png'),
            'redirect_urls': {
                'dashboard': reverse('dashboard:index'),
                'application': reverse('application:form'),
                'company': reverse('company:index'),
                'team': reverse('dashboard:index'),
                'admin': reverse('godmode:index'),
                'staff': reverse('staff:index'),
                'stats': reverse('stats:index'),
                'schedule': reverse('schedule:index'),
                'helper': reverse('helper:index'),
                'logout': reverse('profile:logout'),
            },
            'api': {
                'get_announcement': reverse('announcement:api:announcement-list'),
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
            'is_mentor': profile.is_mentor,
            'is_judge': False,
            'employee_company_access': profile.employee_company_access,
            'state': profile.state,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
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
            'event_logo_text': static('project/img/logo_text.svg'),
            'event_bg': static('project/img/bg.png'),
            'check_token_url': reverse('profile:api:check_token'),
            'reset_email_url': reverse('profile:api:reset_token_email'),
            'error': self.form_error,
            'success': self.form_success,
            'social_urls': {
                'facebook': reverse('social:login', kwargs={'provider': 'facebook'}),
                'github': reverse('social:login', kwargs={'provider': 'github'}),
                'google': reverse('social:login', kwargs={'provider': 'google'}),
            }
        }
        context['login_context'] = json.dumps(login_context)
        return context


class ExportMixin(object):
    """
    Enables exporting in various formats
    Can be used with the DownloadButton.vue component
    """
    renderer_classes = (
        BrowsableAPIRenderer,
        JSONRenderer,
        CSVRenderer,
        NotNestedCSVRenderer,
        TSVRenderer,
        NotNestedTSVRenderer,
        YAMLRenderer,
        XMLRenderer,
        MessagePackRenderer
    )


class PrefetchQuerysetModelMixin(object):
    """Lists a prefetched version of the model list

    To be used with PrefetchMixin
    """

    def get_queryset(self):
        assert self.queryset is not None
        queryset = self.queryset
        if hasattr(self.get_serializer_class(), 'setup_eager_loading'):
            queryset = self.get_serializer().setup_eager_loading(queryset)
        return queryset


class PrefetchMixin(object):

    @classmethod
    def setup_eager_loading(cls, queryset):
        meta = cls.Meta
        if hasattr(meta, "select_related_fields"):
            queryset = queryset.select_related(*meta.select_related_fields)
        if hasattr(meta, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*meta.prefetch_related_fields)
        return queryset
