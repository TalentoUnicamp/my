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
