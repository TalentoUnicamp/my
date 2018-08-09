from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin
from .mixins import HelperContextMixin, IsMentorOrCanSubmitTickets
# Create your views here.


class HelperView(
        IsMentorOrCanSubmitTickets,
        SidebarContextMixin,
        HelperContextMixin,
        UserContextMixin,
        TemplateView):
    template_name = 'helper/helper.html'
    active_tab = 'helper'
