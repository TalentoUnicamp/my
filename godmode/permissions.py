from rest_framework import permissions


class IsAdmin(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.is_superuser


class IsAdminOrUserReadOnly(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False
        profile = request.user.profile
        return (
            profile.is_admin or
            request.method in ('GET', 'HEAD', 'OPTIONS')
        )
