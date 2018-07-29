from rest_framework import serializers
from django.contrib.auth.models import User
from project.mixins import PrefetchMixin
from application.export_serializers import ExportApplicationSerializer


class HackerSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['date_joined']


class HackerApplicationSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    application = ExportApplicationSerializer(source="profile.hacker.application")

    class Meta:
        model = User
        fields = ['date_joined', 'application']
        select_related_fields = ['profile__hacker__application']
