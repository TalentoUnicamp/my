from rest_framework import permissions


class IsEmployee(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.profile.is_employee


class IsAdminOrEmployeeReadOnly(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False
        profile = request.user.profile
        return (
            profile.is_admin or
            request.method in ('GET', 'HEAD', 'OPTIONS') and
            profile.is_employee
        )
