from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet
from project.generics import PrefetchListAPIView
from project.mixins import ExportMixin, PrefetchQuerysetModelMixin
from godmode.permissions import IsAdmin
from .models import Event, Feedback
from .export_serializers import ExportFeedbackSerializer, ExportEventSerializer
from .permissions import CanAttendEvents


class ExportFeedback(ExportMixin, PrefetchListAPIView):
    serializer_class = ExportFeedbackSerializer
    permission_classes = [CanAttendEvents]

    def get_queryset(self):
        event_id = self.kwargs.get('event_id', None)
        event = get_object_or_404(Event, id=event_id)
        if event.speaker != self.request.user.profile:
            return Feedback.objects.none()
        self.queryset = event.feedbacks.all()
        return super().get_queryset()


class ExportEventsViewset(
        ExportMixin,
        PrefetchQuerysetModelMixin,
        ReadOnlyModelViewSet):
    serializer_class = ExportEventSerializer
    permission_classes = [IsAdmin]
    queryset = Event.objects.all()
