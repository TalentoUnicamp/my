from rest_framework import generics
from django.contrib.auth.models import User
from company.permissions import EmployeeHasAccess
from project.mixins import ExportMixin
from .export_serializers import ExportScannedHackersSerializer


class ExportScannedHackers(ExportMixin, generics.ListAPIView):
    serializer_class = ExportScannedHackersSerializer
    permission_classes = [EmployeeHasAccess]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        company = self.request.user.profile.employee.company
        context['company'] = company
        return context

    def get_queryset(self):
        company = self.request.user.profile.employee.company
        return User.objects.filter(profile__scanned_me__scanner__employee__company=company)
