from rest_framework import serializers
from project.mixins import PrefetchMixin
from .models import Scan


class ExportScanSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    scanner_full_name = serializers.CharField(source='scanner.shortcuts.full_name')
    scanner_email = serializers.CharField(source='scanner.user.email')

    class Meta:
        model = Scan
        fields = ['rating', 'comments', 'scanner_full_name', 'scanner_email']
        select_related_fields = ['scanner__user', 'scanner__shortcuts']
