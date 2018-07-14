from rest_framework import permissions
from .models import Settings


class RegistrationOpen(permissions.BasePermission):

    def has_permission(self, request, view):
        return Settings.get().registration_is_open()


class CanConfirm(permissions.BasePermission):

    extend_confirmation = 0

    def has_permission(self, request, view):
        return Settings.get().can_confirm(self.extend_confirmation)


class EventNotFull(permissions.BasePermission):

    def has_permission(self, request, view):
        return not Settings.get().is_full()


class EventIsHappening(permissions.BasePermission):

    def has_permission(self, request, view):
        return Settings.get().hackathon_is_happening()
