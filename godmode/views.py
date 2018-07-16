from django.views.generic import TemplateView
from .mixins import IsAdminMixin, AdminContextMixin
from project.mixins import SidebarContextMixin, UserContextMixin
# Create your views here.


class AdminView(
        IsAdminMixin,
        SidebarContextMixin,
        AdminContextMixin,
        UserContextMixin,
        TemplateView):
    template_name = 'godmode/admin.html'
    active_tab = 'admin'
