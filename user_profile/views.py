from django.views.generic import View
from django.shortcuts import redirect
from django.contrib.messages import add_message, ERROR, SUCCESS
from django.contrib.auth import login
from settings.mixins import RegistrationOpenMixin
from .models import Profile
import time
# Create your views here.


class VerifyEmailView(
        RegistrationOpenMixin,
        View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code', 'invalid')
        try:
            profile = Profile.objects.get(verification_code=code)
            add_message(request, SUCCESS, 'Email verificado')
            profile.verify_email()
            login(request, profile.user)
        except Profile.DoesNotExist:
            add_message(request, ERROR, 'Código inválido')

        return redirect('dashboard:index')


class TokenLoginView(View):

    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token', 'invalid')
        try:
            profile = Profile.objects.get(token=token)
            login(request, profile.user)
            # Force profile update on login
            profile.trigger_update()
        except Profile.DoesNotExist:
            add_message(request, ERROR, 'Token inválido')
            time.sleep(2)
        return redirect('dashboard:index')
