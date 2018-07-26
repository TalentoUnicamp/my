from rest_framework import serializers
from project.mixins import PrefetchMixin
from .models import Application


class ApplicationRetrieveSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):
    unique_id = serializers.CharField(source="hacker.profile.unique_id")
    full_name = serializers.CharField(source="hacker.profile.shortcuts.full_name")
    email = serializers.CharField(source="hacker.profile.user.email")

    class Meta:
        model = Application
        fields = '__all__'
        extra_fields = ['unique_id', 'full_name', 'email']
        select_related_fields = ['hacker__profile__shortcuts', 'hacker__profile__user']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class FormOptionSerializer(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()


class FormOptionsSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True, required=False)
    results = FormOptionSerializer(many=True)
