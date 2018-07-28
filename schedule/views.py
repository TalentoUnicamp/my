from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin
from .mixins import ScheduleContextMixin, CanAttendEvents
# Create your views here.


class ScheduleView(
        SidebarContextMixin,
        CanAttendEvents,
        ScheduleContextMixin,
        UserContextMixin,
        TemplateView):
    template_name = 'schedule/schedule.html'
    active_tab = 'schedule'
