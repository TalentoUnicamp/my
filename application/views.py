from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import ApplicationForm
from project.mixins import SidebarContextMixin, UserContextMixin
from hacker.mixins import IsSubmittedOrIncompleteMixin
from settings.mixins import RegistrationOpenMixin
from django.contrib import messages
# Create your views here.


class ApplicationView(
        RegistrationOpenMixin,
        IsSubmittedOrIncompleteMixin,
        SidebarContextMixin,
        UserContextMixin,
        FormView):
    template_name = 'application/application.html'
    form_class = ApplicationForm
    active_tab = 'application'

    def form_valid(self, form):
        form.save(hacker=self.request.user.profile.hacker)
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Aplicação enviada!")
        return reverse_lazy('dashboard:index')

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        hacker = self.request.user.profile.hacker
        kwargs['instance'] = getattr(hacker, 'application', None)
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['email'] = self.request.user.email
        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        print("here")
        print(context['form'].fields['education'])
        print(context['form'].errors)
        return context
