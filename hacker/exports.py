from rest_framework import generics
from django.contrib.auth.models import User
from rest_condition import Or
from godmode.permissions import IsAdmin
from company.permissions import EmployeeHasAccess
from project.mixins import ExportMixin
from project.generics import PrefetchListAPIView
from .export_serializers import ExportScannedHackersSerializer, ExportAllHackersSerializer


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
        queryset = User.objects.filter(profile__scanned_me__scanner__employee__company=company)
        queryset = self.get_serializer_class().setup_eager_loading(queryset, company)
        return queryset


class ExportAllHackers(ExportMixin, PrefetchListAPIView):
    serializer_class = ExportAllHackersSerializer
    permission_classes = [Or(IsAdmin, EmployeeHasAccess)]
    queryset = User.objects.exclude(profile=None)
