from rest_framework import serializers
from django.contrib.auth.models import User
from application.export_serializers import ExportApplicationSerializer
from user_profile.export_serializers import ExportProfileSerializer
from company.export_serializers import ExportScanSerializer
from company.models import Scan


class ExportScannedHackersSerializer(serializers.Serializer):
    profile = ExportProfileSerializer()
    scan = serializers.SerializerMethodField()
    application = ExportApplicationSerializer(source="profile.hacker.application")

    def get_scan(self, obj):
        scan = Scan.objects.filter(scannee=obj.profile).get(scanner__employee__company=self.context.get('company'))
        return ExportScanSerializer(instance=scan).data

    class Meta:
        model = User
        fields = ['profile', 'scan', 'application']
