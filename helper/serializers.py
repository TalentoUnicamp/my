from rest_framework import serializers
from django.utils import timezone
from project.mixins import PrefetchMixin
from user_profile.serializers import SimpleProfileSerializer
from user_profile.models import Profile
from .models import Ticket, Mentor


class TicketSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    creator = SimpleProfileSerializer(read_only=True)
    claimer = SimpleProfileSerializer(read_only=True)
    claimer_unique_id = serializers.CharField(write_only=True, allow_null=True, required=False)
    state = serializers.CharField(read_only=True)
    set_completed = serializers.BooleanField(required=False, write_only=True)

    def validate_claimer_unique_id(self, value):
        if value is None:
            return None
        if not Profile.objects.filter(unique_id=value).exists():
            raise serializers.ValidationError('Invalid unique id')
        if not Mentor.objects.filter(profile__unique_id=value).exists():
            raise serializers.ValidationError('User is not a mentor')
        return Profile.objects.get(unique_id=value)

    def validate_set_completed(self, value):
        if value:
            return timezone.now()
        return None

    def validate_claimed(self, value):
        return None

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user.profile
        validated_data.pop('claimer_unique_id', None)
        validated_data.pop('set_completed', None)
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        claimer_id = validated_data.pop('claimer_unique_id', False)
        if claimer_id and instance.claimer:
            raise serializers.ValidationError('Ticket already taken')
        if claimer_id is not False:
            validated_data['claimer'] = claimer_id
        if claimer_id is not None and claimer_id is not False:
            validated_data['claimed'] = timezone.now()
        if claimer_id is None:
            validated_data['claimed'] = None
        set_completed = validated_data.pop('set_completed', False)
        if set_completed is None:
            validated_data['completed'] = None
        elif set_completed is not False:
            validated_data['completed'] = set_completed
        return super().update(instance, validated_data)

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['created', 'expires']
        select_related_fields = ['creator__user', 'claimer__user', 'creator__shortcuts', 'claimer__shortcuts']


class MentorSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    profile = SimpleProfileSerializer(read_only=True)
    claimed_tickets = TicketSerializer(source="profile.claimed_tickets", many=True)

    class Meta:
        model = Mentor
        fields = '__all__'
        read_only_fields = ['profile']
        select_related_fields = ['profile__user', 'profile__shortcuts']
        prefetch_related_fields = [
            'profile__claimed_tickets__creator__user',
            'profile__claimed_tickets__creator__shortcuts',
            'profile__claimed_tickets__claimer__user',
            'profile__claimed_tickets__claimer__shortcuts',
        ]
