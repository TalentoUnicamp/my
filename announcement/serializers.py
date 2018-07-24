from rest_framework import serializers
from project.mixins import PrefetchMixin
from .models import Announcement


class AnnouncementSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):
    creator_name = serializers.CharField(source="creator.shortcuts.full_name", read_only=True)
    creator_unique_id = serializers.CharField(source="creator.unique_id", read_only=True)

    class Meta:
        exclude = ['creator']
        read_only_fields = ['created']
        model = Announcement
        select_related_fields = ['creator__shortcuts']

    def create(self, validated_data):
        validated_data['creator'] = self.context['request'].user.profile
        return Announcement.objects.create(**validated_data)
