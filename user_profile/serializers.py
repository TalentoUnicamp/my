from rest_framework import serializers
from project.mixins import PrefetchMixin
from .models import Profile


class ListProfileSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):
    full_name = serializers.CharField(source='shortcuts.full_name')
    email = serializers.EmailField(source='user.email')
    state = serializers.CharField(source='shortcuts.state')
    is_verified = serializers.BooleanField(source='shortcuts.is_verified')
    is_hacker = serializers.BooleanField(source='shortcuts.is_hacker')
    is_staff = serializers.BooleanField(source='shortcuts.is_staff')
    is_admin = serializers.BooleanField(source='shortcuts.is_admin')
    is_employee = serializers.BooleanField(source='shortcuts.is_employee')
    has_facebook = serializers.BooleanField(source='shortcuts.has_facebook')
    has_github = serializers.BooleanField(source='shortcuts.has_github')
    has_google = serializers.BooleanField(source='shortcuts.has_google')

    class Meta:
        model = Profile
        fields = [
            'unique_id',
            'full_name',
            'email',
            'state',
            'is_verified',
            'is_hacker',
            'is_staff',
            'is_admin',
            'is_employee',
            'has_facebook',
            'has_github',
            'has_google'
        ]
        select_related_fields = ['shortcuts', 'user']


class ListHackerProfileSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    full_name = serializers.CharField(source='shortcuts.full_name')
    email = serializers.EmailField(source='user.email')
    state = serializers.CharField(source='shortcuts.state')

    class Meta:
        model = Profile
        fields = ['unique_id', 'email', 'full_name', 'state']
        select_related_fields = ['shortcuts', 'user']
