from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.shortcuts import reverse
import json


class IsAdminMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser


class AdminContextMixin(ContextMixin):
    """Admin context mixin

    Inherit this mixin to get admin data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        admin_context = {
            'api': {
                'list_profiles': reverse('profile:api:list_profiles'),
                'toggle_is_hacker': reverse('hacker:api:toggle_is_hacker'),
                'toggle_is_staff': reverse('staff:api:toggle_is_staff'),

                'toggle_is_admin': reverse('godmode:api:toggle_is_admin'),
                'delete_user': reverse('godmode:api:delete_user', args=[0])[:-2],
                'batch_create_users': reverse('godmode:api:batch_create_users'),

                'toggle_is_mentor': reverse('helper:api:toggle_is_mentor'),

                'list_companies': reverse('company:api:company-list'),
                'create_company': reverse('company:api:company-list'),
                'delete_company': reverse('company:api:company-detail', args=[0])[:-2],

                'list_employees': reverse('company:api:employee-list'),
                'create_employee': reverse('company:api:employee-list'),
                'delete_employee': reverse('company:api:employee-detail', args=[0])[:-2],

                'fetch_checkin_employee': reverse('company:api:fetch_checkin_employee'),
                'checkin_employee': reverse('company:api:checkin_employee'),

                'update_settings': reverse('settings:api:get_update'),

                'list_announcement': reverse('announcement:api:announcement-list'),
                'create_announcement': reverse('announcement:api:announcement-list'),
                'delete_announcement': reverse('announcement:api:announcement-detail', args=[0])[:-2],
            }
        }
        context['admin_context'] = json.dumps(admin_context)
        return context
