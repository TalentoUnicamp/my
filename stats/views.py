from django.views.generic import TemplateView
from project.mixins import SidebarContextMixin, UserContextMixin
from .mixins import StatsContextMixin
# Create your views here.


class StatsView(
        SidebarContextMixin,
        StatsContextMixin,
        UserContextMixin,
        TemplateView):
    template_name = 'stats/stats.html'
    active_tab = 'stats'
