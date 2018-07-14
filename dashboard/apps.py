from django.apps import AppConfig
from project.custom_appconf import NoPrefixAppConf


class DashboardConfig(AppConfig):
    name = 'dashboard'


class DashboardSettings(NoPrefixAppConf):
    pass
