from rest_framework import permissions


class IsEmployee(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.profile.is_employee


class EmployeeHasAccess(IsEmployee):
    access_level = 0

    def has_permission(self, request, view):
        is_employee = super().has_permission(request, view)
        if not is_employee:
            return False
        company_access = request.user.profile.employee.company.access_level
        return company_access >= self.access_level


class IsAdminOrEmployeeReadOnly(permissions.IsAuthenticated):
    access_level = 0

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        if not is_authenticated:
            return False
        profile = request.user.profile
        employee_has_access = False
        if profile.is_employee:
            if profile.employee.company.access_level >= self.access_level:
                employee_has_access = True
        return (
            profile.is_admin or
            request.method in ('GET', 'HEAD', 'OPTIONS') and
            employee_has_access
        )
