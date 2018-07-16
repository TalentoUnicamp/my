from rest_framework import serializers
from .models import Profile


class ListProfileSerializer(serializers.ModelSerializer):

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


class ListHackerProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['unique_id', 'email', 'full_name', 'state']
