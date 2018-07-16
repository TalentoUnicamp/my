from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.shortcuts import reverse
import json


class IsEmployeeMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.is_employee


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
            'api': {
                'fetch_scan_hacker': reverse('company:api:fetch_scan_hacker'),
                'scan_hacker': reverse('company:api:scan_hacker'),
            }
        }
        context = super().get_context_data(**kwargs)
        context['company_context'] = json.dumps(company_context)
        return context
