from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.shortcuts import reverse
import json


class IsMentorMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.is_mentor


class IsMentorOrSuperuserMixin(IsMentorMixin):
    def test_func(self):
        return super().test_func() or self.request.user.is_superuser


class IsMentorOrCanSubmitTickets(LoginRequiredMixin, UserPassesTestMixin):
    access_level = 0

    def test_func(self):
        # Only admins and employees can submit tickets, or mentors
        profile = self.request.user.profile
        has_employee_access = profile.is_employee
        if has_employee_access:
            company_access = profile.employee.company.access_level
            has_employee_access = company_access >= self.access_level
        return (
            profile.is_staff or
            profile.is_mentor or
            has_employee_access
        )


class HelperContextMixin(ContextMixin):
    """Helper context mixin

    Inherit this mixin to get helper data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        helper_context = {
            'api': {
                'last_ticket': reverse('helper:api:ticket-last-ticket'),
                'list_tickets': reverse('helper:api:ticket-list'),
                'online_mentors': reverse('helper:api:online_mentors-list'),
                'list_mentors': reverse('helper:api:mentor-list'),
                'self_mentor': reverse('helper:api:self_mentor'),
            }
        }
        context['helper_context'] = json.dumps(helper_context)
        return context
