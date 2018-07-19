from rest_framework import serializers
from .models import Profile


class ExportProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ['unique_id', 'email', 'full_name', 'state']
