from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin
from .mixins import CompanyContextMixin, IsEmployeeMixin
# Create your views here.


class CompanyView(
        IsEmployeeMixin,
        SidebarContextMixin,
        CompanyContextMixin,
        UserContextMixin,
        TemplateView):
    template_name = 'company/company.html'
    active_tab = 'company'
