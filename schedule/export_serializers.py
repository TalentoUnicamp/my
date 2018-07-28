from rest_framework import serializers
from project.mixins import PrefetchMixin
from .models import Feedback


class ExportFeedbackSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    event = serializers.CharField(source='event.name')

    class Meta:
        model = Feedback
        exclude = ['attendee', 'id']
        select_related_fields = ['event']
