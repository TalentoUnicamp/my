from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin
from .mixins import DashboardContextMixin
from settings.mixins import SettingsContextMixin


class Dashboard(
        SidebarContextMixin,
        DashboardContextMixin,
        UserContextMixin,
        SettingsContextMixin,
        TemplateView):

    template_name = 'dashboard/dashboard.html'
    active_tab = 'dashboard'
