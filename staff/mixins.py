from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import ContextMixin
from django.shortcuts import reverse
import json


class IsStaffMixin(UserPassesTestMixin):
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
                'list_hackers': reverse('hacker:api:list_hackers'),
            }
        }
        context['staff_context'] = json.dumps(staff_context)
        return context
