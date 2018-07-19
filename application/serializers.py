from rest_framework import serializers
from .models import Application


class ApplicationRetrieveSerializer(serializers.ModelSerializer):
    unique_id = serializers.CharField(source="hacker.profile.unique_id")
    full_name = serializers.CharField(source="hacker.profile.full_name")
    email = serializers.CharField(source="hacker.profile.email")

    class Meta:
        model = Application
        fields = '__all__'
        extra_fields = ['unique_id', 'full_name', 'email']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields
