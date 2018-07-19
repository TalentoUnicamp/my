from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin
from .mixins import DashboardContextMixin


class Dashboard(
        SidebarContextMixin,
        DashboardContextMixin,
        UserContextMixin,
        TemplateView):

    template_name = 'dashboard/dashboard.html'
    active_tab = 'dashboard'
