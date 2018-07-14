from rest_framework import permissions


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.profile.is_staff


class IsStaffOrSuperuser(IsStaff):

    def has_permission(self, request, view):
        return super().has_permission(request, view) or request.user.is_superuser
