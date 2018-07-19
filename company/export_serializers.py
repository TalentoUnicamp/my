from rest_framework import serializers
from .models import Scan


class ExportScanSerializer(serializers.ModelSerializer):

    scanner_name = serializers.CharField(source='scanner.full_name')
    scanner_email = serializers.CharField(source='scanner.email')

    class Meta:
        model = Scan
        fields = ['rating', 'comments', 'scanner_name', 'scanner_email']
