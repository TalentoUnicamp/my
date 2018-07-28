from rest_condition import Or
from godmode.permissions import IsAdmin
from hacker.permissions import IsCheckedin, IsConfirmed
from staff.permissions import IsStaff
from company.permissions import EmployeeHasAccess

CanAttendEvents = Or(
    IsAdmin,
    IsCheckedin,
    IsConfirmed,
    IsStaff,
    EmployeeHasAccess
)
