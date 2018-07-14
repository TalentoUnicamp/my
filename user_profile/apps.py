from django.apps import AppConfig
from django.urls import reverse_lazy
from project.custom_appconf import NoPrefixAppConf


class AppConf(AppConfig):
    name = 'user_profile'


class AppSettings(NoPrefixAppConf):
    TOKEN_SIZE = 10
    PROFILE_REDIRECT_URL = reverse_lazy('dashboard:index')
