from rest_framework import permissions
from rest_condition import Or
from company.permissions import EmployeeHasAccess
from staff.permissions import IsStaff


class IsMentor(permissions.IsAuthenticated):

    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)
        return is_authenticated and request.user.profile.is_mentor


CanSubmitTickets = Or(
    EmployeeHasAccess,
    IsMentor,
    IsStaff
)
