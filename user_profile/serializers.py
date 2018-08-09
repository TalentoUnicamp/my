from rest_framework import serializers
from django.db.models.functions import Concat
from django.db.models import CharField, Value
from project.mixins import PrefetchMixin
from .models import Profile


class SimpleProfileSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    full_name = serializers.CharField(source='shortcuts.full_name')
    email = serializers.EmailField(source='user.email')
    state = serializers.CharField(source='shortcuts.state')

    class Meta:
        model = Profile
        fields = ['unique_id', 'full_name', 'email', 'state']
        select_related_fields = ['shortcuts', 'user']


class ListProfileSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):
    full_name = serializers.CharField(source='shortcuts.full_name')
    email = serializers.EmailField(source='user.email')
    state = serializers.CharField(source='shortcuts.state')
    is_verified = serializers.BooleanField(source='shortcuts.is_verified')
    is_hacker = serializers.BooleanField(source='shortcuts.is_hacker')
    is_staff = serializers.BooleanField(source='shortcuts.is_staff')
    is_mentor = serializers.BooleanField(source='shortcuts.is_mentor')
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
            'is_mentor',
            'is_employee',
            'has_facebook',
            'has_github',
            'has_google'
        ]
        select_related_fields = ['shortcuts', 'user']


class ListHackerProfileSerializer(SimpleProfileSerializer):
    pass


class SUIProfileListSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    name = serializers.CharField()
    value = serializers.EmailField(source='unique_id')

    def setup_eager_loading(self, queryset):
        meta = self.Meta
        if hasattr(meta, "select_related_fields"):
            queryset = queryset.select_related(*meta.select_related_fields)
        if hasattr(meta, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*meta.prefetch_related_fields)

        queryset = queryset.annotate(
            name=Concat('shortcuts__full_name', Value(' ('), 'user__email', Value(')'), output_field=CharField())
        )
        return queryset

    class Meta:
        model = Profile
        fields = ['name', 'value']
        select_related_fields = ['shortcuts', 'user']
