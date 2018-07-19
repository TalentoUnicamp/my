from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.shortcuts import reverse
import json


class IsStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.is_staff


class IsStaffOrSuperuserMixin(IsStaffMixin):
    def test_func(self):
        return super().test_func() or self.request.user.is_superuser


class StaffContextMixin(ContextMixin):
    """Staff context mixin

    Inherit this mixin to get staff data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_context = {
            'api': {
                'list_hacker_profiles': reverse('profile:api:list_hacker_profiles'),
                'create_blank_hacker': reverse('staff:api:create_blank_hacker'),
                'fetch_checkin_hacker': reverse('hacker:api:fetch_checkin_hacker'),
                'checkin_hacker': reverse('hacker:api:checkin_hacker'),
                'admit_hacker': reverse('hacker:api:admit_hacker'),
                'decline_hacker': reverse('hacker:api:decline_hacker'),
                'unwaitlist_hacker': reverse('hacker:api:unwaitlist_hacker'),

                'view_application': reverse('application:api:view_application', args=[0])[:-2],
            }
        }
        context['staff_context'] = json.dumps(staff_context)
        return context
