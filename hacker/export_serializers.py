from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Prefetch
from project.mixins import PrefetchMixin
from application.export_serializers import ExportApplicationSerializer
from user_profile.export_serializers import ExportProfileSerializer
from company.export_serializers import ExportScanSerializer
from company.models import Scan


class ExportScannedHackersSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):
    profile = ExportProfileSerializer()
    scan = serializers.SerializerMethodField()
    application = ExportApplicationSerializer(source="profile.hacker.application")

    def get_scan(self, obj):
        scan = obj.profile.scan[0]
        return ExportScanSerializer(instance=scan).data

    @classmethod
    def setup_eager_loading(self, queryset, company):
        meta = self.Meta

        if hasattr(meta, "select_related_fields"):
            queryset = queryset.select_related(*meta.select_related_fields)
        if hasattr(meta, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*meta.prefetch_related_fields)

        company_scans = Scan.objects.filter(scanner__employee__company=company)
        company_scans = company_scans.select_related(*ExportScanSerializer.Meta.select_related_fields)

        queryset = queryset.prefetch_related(
            Prefetch('profile__scanned_me', queryset=company_scans, to_attr='scan')
        )

        return queryset

    class Meta:
        model = User
        fields = ['profile', 'scan', 'application']
        select_related_fields = ['profile__hacker__application', 'profile__shortcuts']


class ExportAllHackersSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):
    profile = ExportProfileSerializer()
    application = ExportApplicationSerializer(source="profile.hacker.application")

    class Meta:
        model = User
        fields = ['profile', 'application']
        select_related_fields = ['profile__hacker__application', 'profile__shortcuts']
