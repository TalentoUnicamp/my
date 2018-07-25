from rest_framework import permissions


class UserReadOnly(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.method in ('GET', 'HEAD', 'OPTIONS')
