from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.messages import get_messages
from .mixins import LoginContextMixin


class LoginView(LoginContextMixin, TemplateView):
    template_name = 'project/login.html'

    def get_context_data(self, **kwargs):
        messages = ''
        for message in get_messages(self.request):
            messages += message.message + '\n'
        self.form_error = messages
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.PROFILE_REDIRECT_URL)
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
