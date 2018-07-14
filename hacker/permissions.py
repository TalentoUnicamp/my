from rest_framework import permissions


class IsHacker(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.is_hacker


class IsCheckedin(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'checked_in'


class IsAdmitted(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'admitted'


class IsWithdraw(IsHacker):

    def has_permission(self, request, view):
        parent = super().has_permission(request, view)
        return parent and request.user.profile.state == 'withdraw'
