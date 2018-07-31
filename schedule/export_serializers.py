from rest_framework import serializers
from project.mixins import PrefetchMixin
from user_profile.export_serializers import ExportProfileSerializer
from .serializers import FeedbackSerializer
from .models import Feedback, Event


class ExportFeedbackSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    event = serializers.CharField(source='event.name')

    class Meta:
        model = Feedback
        exclude = ['attendee', 'id']
        select_related_fields = ['event']


class ExportEventSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    attendees = ExportProfileSerializer(many=True)
    attended = ExportProfileSerializer(many=True)
    speaker = ExportProfileSerializer()
    feedbacks = FeedbackSerializer(many=True)

    class Meta:
        model = Event
        fields = '__all__'
        select_related_fields = ['speaker__shortcuts', 'speaker__user']
        prefetch_related_fields = [
            'feedbacks__event',
            'attendees__shortcuts',
            'attendees__user',
            'attended__shortcuts',
            'attended__user'
        ]
