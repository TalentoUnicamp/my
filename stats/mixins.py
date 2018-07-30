from django.views.generic.base import ContextMixin
from django.shortcuts import reverse
import json
from company.mixins import EmployeeHasAccessMixin


class StatsContextMixin(ContextMixin):
    """Stats context mixin

    Inherit this mixin to get stats data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats_context = {
            'api': {
                'hacker_stats': reverse('stats:api:hacker_stats'),
                'hacker_signup_list': reverse('stats:api:hacker_signup_list'),
                'hacker_application_list': reverse('stats:api:hacker_application_list'),
            },
            'exports': {
                'all_hackers': reverse('hacker:exports:all_hackers'),
            }
        }
        context['stats_context'] = json.dumps(stats_context)
        return context


class IsAdminOrStaffOrEmployeeWithAccessMixin(EmployeeHasAccessMixin):

    def test_func(self):
        employee_with_access = super().test_func()
        is_staff = self.request.user.profile.is_staff
        is_admin = self.request.user.profile.is_admin
        return employee_with_access or is_staff or is_admin
