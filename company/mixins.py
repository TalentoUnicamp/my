from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.shortcuts import reverse
import json


class IsEmployeeMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.is_employee


class EmployeeHasAccessMixin(IsEmployeeMixin):
    access_level = 0

    def test_func(self):
        if not super().test_func():
            # if not employee, return False
            return False
        company_access = self.request.user.profile.employee.company.access_level
        return company_access >= self.access_level


class CompanyContextMixin(LoginRequiredMixin, ContextMixin):
    """Company Context

    Inherit this mixin to automatically get the context required for
    the employee views
    """

    active_tab = ''

    def get_context_data(self, **kwargs):
        user = self.request.user
        profile = user.profile
        company = profile.employee.company
        company_context = {
            'active_tab': self.active_tab,
            'company_name': company.name,
            'company_access_level': company.access_level,
            'api': {
                'fetch_scan_hacker': reverse('company:api:fetch_scan_hacker'),
                'scan_hacker': reverse('company:api:scan_hacker'),

                'scan_list': reverse('company:api:scan-list'),
                'scan_destroy': reverse('company:api:scan-detail', args=[0])[:-2],
                'scan_update': reverse('company:api:scan-detail', args=[0])[:-2],
            },
            'exports': {
                'scanned_hackers': reverse('hacker:exports:scanned_hackers')
            }
        }
        context = super().get_context_data(**kwargs)
        context['company_context'] = json.dumps(company_context)
        return context
