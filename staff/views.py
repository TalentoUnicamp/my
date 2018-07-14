from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin
from .mixins import StaffContextMixin
# Create your views here.


class StaffView(
        SidebarContextMixin,
        StaffContextMixin,
        UserContextMixin,
        TemplateView):
    template_name = 'staff/staff.html'
    active_tab = 'staff'
