from rest_framework import permissions


class IsHacker(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.profile.is_hacker


class IsCheckedin(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'checked_in'


class IsAdmitted(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'admitted'


class IsConfirmed(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'confirmed'


class IsWithdraw(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'withdraw'
