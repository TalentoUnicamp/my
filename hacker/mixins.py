from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class IsHackerMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.profile.is_hacker


class IsCheckedinMixin(IsHackerMixin):
    def test_func(self):
        parent = super().test_func()
        return parent and self.request.user.profile.state == 'checked_in'


class IsAdmittedMixin(IsHackerMixin):
    def test_func(self):
        parent = super().test_func()
        return parent and self.request.user.profile.state == 'checked_in'


class IsSubmittedOrIncompleteMixin(IsHackerMixin):
    def test_func(self):
        parent = super().test_func()
        return parent and (
            self.request.user.profile.state == 'submitted'or
            self.request.user.profile.state == 'incomplete' or
            self.request.user.profile.state == 'unverified')
