from rest_framework import serializers
from project.mixins import PrefetchMixin
from .models import Profile


class ExportProfileSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    full_name = serializers.CharField(source='shortcuts.full_name')
    email = serializers.EmailField(source='user.email')
    state = serializers.CharField(source='shortcuts.state')

    class Meta:
        model = Profile
        fields = ['unique_id', 'email', 'full_name', 'state']
        select_related_fields = ['shortcuts', 'user']
