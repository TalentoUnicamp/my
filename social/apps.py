from django.conf import settings
from django.apps import AppConfig
from project.custom_appconf import NoPrefixAppConf
import os


class SocialConfig(AppConfig):
    name = 'social'


class SocialSettings(NoPrefixAppConf):
    FACEBOOK_KEY = os.environ.get('FACEBOOK_KEY', '')
    FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET', '')
    FACEBOOK_PERMISSIONS = eval(os.environ.get('FACEBOOK_PERMISSIONS', '["email"]'))
    FACEBOOK_HANDLE = os.environ.get('FACEBOOK_HANDLE', 'https://facebook.com/')
    GITHUB_KEY = os.environ.get('GITHUB_KEY', '')
    GITHUB_SECRET = os.environ.get('GITHUB_SECRET', '')
    GITHUB_PERMISSIONS = eval(os.environ.get('GITHUB_PERMISSIONS', '["email"]'))
    GOOGLE_KEY = os.environ.get('GOOGLE_KEY', '')
    GOOGLE_SECRET = os.environ.get('GOOGLE_SECRET', '')
    GOOGLE_PERMISSIONS = eval(os.environ.get('GOOGLE_PERMISSIONS', '["profile", "email"]'))
