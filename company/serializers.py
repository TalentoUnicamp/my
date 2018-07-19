from rest_framework import serializers
from user_profile.models import Profile
from .models import Company, Employee, Scan


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['id', 'name', 'access_level']
        model = Company


class ScanSerializer(serializers.ModelSerializer):

    scannee_full_name = serializers.CharField(source='scannee.full_name')
    scannee_unique_id = serializers.CharField(source='scannee.unique_id')
    scannee_email = serializers.CharField(source='scannee.email')
    scanner_full_name = serializers.CharField(source='scanner.full_name')
    scanner_unique_id = serializers.CharField(source='scanner.unique_id')
    scanner_email = serializers.CharField(source='scanner.email')

    class Meta:
        fields = ['id', 'rating', 'comments', 'scannee_full_name', 'scannee_unique_id', 'scannee_email', 'scanner_full_name', 'scanner_unique_id', 'scanner_email']
        model = Scan


class ReadEmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='profile.full_name')
    email = serializers.CharField(source='profile.email')
    unique_id = serializers.CharField(source='profile.unique_id')
    company_name = serializers.CharField(source='company.name')

    class Meta:
        fields = ['full_name', 'email', 'unique_id', 'company_name']
        model = Employee


class CreateEmployeeSerializer(serializers.ModelSerializer):
    unique_id = serializers.CharField(source='profile.unique_id')
    company_id = serializers.IntegerField(source='company.id')

    def validate_unique_id(self, value):
        if not Profile.objects.filter(unique_id=value).exists():
            raise serializers.ValidationError('Invalid unique id')
        if Employee.objects.filter(profile__unique_id=value).exists():
            raise serializers.ValidationError('User is already an employee')
        return value

    def validate_company_id(self, value):
        if not Company.objects.filter(id=value).exists():
            raise serializers.ValidationError('Invalid company id')
        return value

    def create(self, validated_data):
        unique_id = validated_data.get('profile').get('unique_id')
        company_id = validated_data.get('company').get('id')
        profile = Profile.objects.get(unique_id=unique_id)
        company = Company.objects.get(id=company_id)
        return Employee.objects.create(profile=profile, company=company)

    class Meta:
        fields = ['unique_id', 'company_id']
        model = Employee
