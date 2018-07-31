from rest_framework import serializers
from django.db.models import Count, Avg, Prefetch
from project.mixins import PrefetchMixin
from user_profile.serializers import SimpleProfileSerializer
from user_profile.models import Profile
from .models import Event, Feedback


class EventSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    speaker_unique_id = serializers.CharField(write_only=True, required=False, allow_null=True, allow_blank=True)
    speaker = SimpleProfileSerializer(read_only=True)
    n_attendees = serializers.IntegerField(read_only=True)
    n_attended = serializers.IntegerField(read_only=True)

    @classmethod
    def setup_eager_loading(self, queryset):
        meta = self.Meta
        if hasattr(meta, "select_related_fields"):
            queryset = queryset.select_related(*meta.select_related_fields)
        if hasattr(meta, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*meta.prefetch_related_fields)

        queryset = queryset.annotate(
            n_attendees=Count('attendees', distinct=True),
            n_attended=Count('attended', distinct=True),
        )
        return queryset

    def validate_speaker_unique_id(self, value):
        if not value:
            return None
        if not Profile.objects.filter(unique_id=value).exists():
            raise serializers.ValidationError('Invalid speaker unique id')
        return value

    def create(self, validated_data):
        unique_id = validated_data.pop('speaker_unique_id', None)
        if unique_id:
            validated_data['speaker'] = Profile.objects.get(unique_id=unique_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # If switching from requiring register to not, clear relations
        require_register = validated_data.get('require_register', None)
        if require_register is not None and not require_register and instance.require_register:
            print("NONNONNONONO")
            instance.attendees.clear()
            instance.attended.clear()
            instance.feedbacks.all().delete()
        unique_id = validated_data.pop('speaker_unique_id', False)
        if unique_id or unique_id is None:
            if unique_id is None:
                validated_data['speaker'] = None
            else:
                validated_data['speaker'] = Profile.objects.get(unique_id=unique_id)
        return super().update(instance, validated_data)

    class Meta:
        exclude = ['attendees', 'attended']
        read_only_fields = ['id']
        model = Event
        select_related_fields = ['speaker__shortcuts', 'speaker__user']


class FeedbackSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    event_id = serializers.IntegerField(source='event.id', required=False)

    def validate_event_id(self, value):
        if not Event.objects.filter(id=value):
            raise serializers.ValidationError('Invalid event id')
        return value

    def create(self, validated_data):
        event_id = validated_data.pop('event').get('id', None)
        event = Event.objects.get(id=event_id)
        attendee = self.context['request'].user.profile
        validated_data['event'] = event
        validated_data['attendee'] = attendee
        rating = validated_data.get('rating', None)
        validated_data['rating'] = None if not rating else rating
        feedback = Feedback.objects.filter(event=event).filter(attendee=attendee)
        if feedback.exists():
            return self.update(feedback.first(), validated_data)
        return super().create(validated_data)

    class Meta:
        model = Feedback
        exclude = ['event', 'attendee']
        select_related_fields = ['event']


class FullEventSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    speaker_unique_id = serializers.CharField(write_only=True, required=False)
    speaker = SimpleProfileSerializer(read_only=True)
    n_attendees = serializers.IntegerField(read_only=True)
    n_attended = serializers.IntegerField(read_only=True)
    avg_rating = serializers.FloatField(read_only=True)
    feedbacks = FeedbackSerializer(many=True, read_only=True)

    @classmethod
    def setup_eager_loading(self, queryset):
        meta = self.Meta
        if hasattr(meta, "select_related_fields"):
            queryset = queryset.select_related(*meta.select_related_fields)
        if hasattr(meta, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*meta.prefetch_related_fields)

        queryset = queryset.annotate(
            n_attendees=Count('attendees', distinct=True),
            n_attended=Count('attended', distinct=True),
            avg_rating=Avg('feedbacks__rating', distinct=True)
        )
        return queryset

    def validate_speaker_unique_id(self, value):
        if not value:
            return None
        if not Profile.objects.filter(unique_id=value).exists():
            raise serializers.ValidationError('Invalid speaker unique id')
        return value

    def create(self, validated_data):
        unique_id = validated_data.pop('speaker_unique_id', None)
        if unique_id:
            validated_data['speaker'] = Profile.objects.get(unique_id=unique_id)
        return super().create(validated_data)

    class Meta:
        exclude = ['attendees', 'attended']
        model = Event
        select_related_fields = ['speaker__shortcuts', 'speaker__user']
        prefetch_related_fields = ['feedbacks__event']


class AttendedEventSerializer(
        PrefetchMixin,
        serializers.ModelSerializer):

    speaker = SimpleProfileSerializer(read_only=True)
    n_attendees = serializers.IntegerField(read_only=True)
    n_attended = serializers.IntegerField(read_only=True)
    feedbacks = FeedbackSerializer(read_only=True, many=True)

    def setup_eager_loading(self, queryset):
        meta = self.Meta

        attendee = self.context['request'].user.profile
        feedbacks_queryset = Feedback.objects.filter(attendee=attendee)
        queryset = queryset.prefetch_related(
            Prefetch('feedbacks', queryset=feedbacks_queryset)
        )

        if hasattr(meta, "select_related_fields"):
            queryset = queryset.select_related(*meta.select_related_fields)
        if hasattr(meta, "prefetch_related_fields"):
            queryset = queryset.prefetch_related(*meta.prefetch_related_fields)

        queryset = queryset.annotate(
            n_attendees=Count('attendees', distinct=True),
            n_attended=Count('attended', distinct=True),
        )
        return queryset

    class Meta:
        exclude = ['attendees', 'attended']
        model = Event
        select_related_fields = ['speaker__shortcuts', 'speaker__user']
        prefetch_related_fields = ['feedbacks__event']
