from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.shortcuts import reverse
import json


class CanAttendEvents(LoginRequiredMixin, UserPassesTestMixin):
    access_level = 0

    def test_func(self):
        profile = self.request.user.profile
        has_employee_access = profile.is_employee
        if has_employee_access:
            company_access = profile.employee.company.access_level
            has_employee_access = company_access >= self.access_level
        return (
            profile.is_staff or
            profile.is_mentor or
            profile.is_admin or
            has_employee_access or
            profile.state == 'checkedin' or
            profile.state == 'confirmed'
        )


class ScheduleContextMixin(ContextMixin):
    """Schedule context mixin

    Inherit this mixin to get schedule data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedule_context = {
            'api': {
                'list_events': reverse('schedule:api:event-list'),
                'get_event': reverse('schedule:api:event-detail', args=[0])[:-2],
                'create_event': reverse('schedule:api:event-list'),
                'delete_event': reverse('schedule:api:event-detail', args=[0])[:-2],

                'my_list_events': reverse('schedule:api:my_event-list'),
                'my_update_event': reverse('schedule:api:my_event-detail', args=[0])[:-2],
                'my_delete_event': reverse('schedule:api:my_event-detail', args=[0])[:-2],

                'registered_list_events': reverse('schedule:api:registered_event-list'),

                'not_registered_list_events': reverse('schedule:api:not_registered_event-list'),

                'attended_list_events': reverse('schedule:api:attended_event-list'),

                'my_full_list_events': reverse('schedule:api:my_full_event-list'),

                'checkinable_events': reverse('schedule:api:checkinable_events-list'),

                'create_feedback': reverse('schedule:api:feedback-list'),

                'attend_event': reverse('schedule:api:attend_event'),
                'neglect_event': reverse('schedule:api:neglect_event'),
                'fetch_checkin': reverse('schedule:api:fetch_checkin'),
                'checkin': reverse('schedule:api:checkin'),

                'sui_list_profiles': reverse('profile:api:sui_list_profiles'),
            },
            'exports': {
                'feedback': reverse('schedule:exports:feedback', args=[0])[:-2],
                'event_list': reverse('schedule:exports:events-list'),
                'event_get': reverse('schedule:exports:events-detail', args=[0])[:-2],
            }
        }
        context['schedule_context'] = json.dumps(schedule_context)
        return context
