from django.conf import settings
from django.views.generic import RedirectView
from .providers import facebook, github, google
from .util import decode_state_data, login_canceled


# Create your views here.
providers = {
    'facebook': facebook,
    'github': github,
    'google': google,
}


class SocialLogin(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        provider = providers[kwargs['provider']]
        return provider.auth_url(self.request)


class SocialLoginResponse(RedirectView):
    max_code_redirects = 3

    def get_redirect_url(self, *args, **kwargs):
        provider = providers[kwargs['provider']]
        code = self.request.GET.get('code', False)
        state_data = decode_state_data(self.request.GET.get('state', False))
        redirected = state_data.get('redirected', False)
        next_url = state_data.get('next_url', False)
        if not code or redirected and int(redirected) >= self.max_code_redirects:
            self.request = login_canceled(self.request)
            return settings.LOGIN_REDIRECT_URL
        else:
            print(self.request.user)
            response = provider.login_successful(code, self.request)
            if response == 'auth code used' or response == 'token missing':
                # if the auth code has already been used, redirect
                return provider.code_already_used_url(next_url, redirected)
            self.request = response
        if next_url:
            return next_url
        return settings.LOGIN_REDIRECT_URL
