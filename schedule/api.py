from rest_framework import views, viewsets, response, mixins
from rest_framework.permissions import IsAuthenticated
from rest_condition import And, Or
from project.mixins import PrefetchQuerysetModelMixin
from project.permissions import IsReadyOnlyRequest
from user_profile.models import Profile
from godmode.permissions import IsAdmin
from staff.permissions import IsStaff
from .serializers import EventSerializer, FullEventSerializer, FeedbackSerializer, AttendedEventSerializer
from .models import Event, Feedback
from .permissions import CanAttendEvents


class EventViewset(
        PrefetchQuerysetModelMixin,
        viewsets.ModelViewSet):
    """Event
    Get all events and their basic data
    authenticated can read, admin can edit
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [
        Or(
            And(
                CanAttendEvents,
                And(IsAuthenticated, IsReadyOnlyRequest)
            ),
            IsAdmin
        )
    ]


class MyEventViewset(
        PrefetchQuerysetModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """My events
    List basic info about the events i'll be hosting
    authenticated can do everything
    """
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [CanAttendEvents]

    def get_queryset(self):
        self.queryset = self.queryset.filter(speaker=self.request.user.profile)
        return super().get_queryset()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        data = dict(request.data)
        data.pop('speaker_unique_id', None)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)


class RegisteredEventViewset(
        PrefetchQuerysetModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """Registered events
    List basic info about the events i'll be attending
    authenticated can do all
    """

    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [CanAttendEvents]

    def get_queryset(self):
        attendee = self.request.user.profile
        self.queryset = self.queryset.filter(attendees__in=[attendee]).exclude(attended__in=[attendee])
        return super().get_queryset()


class NotRegisteredEventViewset(
        PrefetchQuerysetModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """Not Registered events
    List basic info about the events i'll not be attending
    authenticated can do all
    """

    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [CanAttendEvents]

    def get_queryset(self):
        self.queryset = self.queryset.exclude(attendees__in=[self.request.user.profile])
        return super().get_queryset()


class AttendedEventViewset(
        PrefetchQuerysetModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """Registered events
    List basic info about the events i attended and my feedback on them
    authenticated can do all
    """

    serializer_class = AttendedEventSerializer
    queryset = Event.objects.all()
    permission_classes = [CanAttendEvents]

    def get_queryset(self):
        self.queryset = self.queryset.filter(attended__in=[self.request.user.profile])
        return super().get_queryset()


class FullEventViewset(
        PrefetchQuerysetModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """Full event
    List full info about events
    only admin
    """

    serializer_class = FullEventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAdmin]


class MyFullEventViewset(
        PrefetchQuerysetModelMixin,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        viewsets.GenericViewSet):
    """Full event
    List full info about events i'll be hosting
    authenticated can do all
    """

    serializer_class = FullEventSerializer
    queryset = Event.objects.all()
    permission_classes = [CanAttendEvents]

    def get_queryset(self):
        self.queryset = self.queryset.filter(speaker=self.request.user.profile)
        return super().get_queryset()


class CheckinableEventViewset(
        PrefetchQuerysetModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    """Full event
    List info about events that require registration
    only staff
    """

    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsStaff]

    def get_queryset(self):
        self.queryset = self.queryset.filter(require_register=True)
        return super().get_queryset()


class FeedbackViewset(
        PrefetchQuerysetModelMixin,
        mixins.UpdateModelMixin,
        mixins.CreateModelMixin,
        viewsets.GenericViewSet):

    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()
    permission_classes = [CanAttendEvents]

    def get_queryset(self):
        self.queryset = self.queryset.filter(attendee=self.request.user.profile)
        return super().get_queryset()

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        data = dict(request.data)
        data.pop('event_id', None)
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return response.Response(serializer.data)


class AttendEvent(views.APIView):
    """Attend event
    """
    permission_classes = [CanAttendEvents]

    def post(self, request):
        event_id = request.data.get('event_id', None)
        event = Event.objects.filter(pk=event_id)
        if not event.exists():
            return response.Response({'message': 'Evento inválido'}, status=400)
        event = event[0]
        added = event.add_attendee(request.user.profile)
        if not added:
            return response.Response({'message': 'Evento cheio'}, status=403)
        return response.Response({'message': 'Registrado'})


class NeglectEvent(views.APIView):
    permission_classes = [CanAttendEvents]

    def post(self, request):
        event_id = request.data.get('event_id', None)
        event = Event.objects.filter(pk=event_id)
        if not event.exists():
            return response.Response({'message': 'Evento inválido'}, status=400)
        event = event[0]
        removed = event.remove_attendee(request.user.profile)
        if not removed:
            return response.Response({'message': 'Participante não se registrou para esse evento'}, status=403)
        return response.Response({'message': 'Registrado'})


class FetchCheckinAttendee(views.APIView):
    permission_classes = [IsStaff]

    def post(self, request):
        event_id = request.data.get('event_id', None)
        unique_id = request.data.get('unique_id', None)
        print(event_id, unique_id)
        event = Event.objects.filter(pk=event_id)
        if not event.exists():
            return response.Response({'status': 'error', 'title': 'Opa!', 'message': 'Evento inválido'})
        attendee = Profile.objects.filter(unique_id=unique_id)
        if not attendee.exists():
            return response.Response({'status': 'error', 'title': 'Opa!', 'message': 'Participante inválido'})
        event = event[0]
        attendee = attendee[0]
        registered = event.attendee_registered(attendee)
        if not registered:
            return response.Response({'status': 'error', 'title': 'Opa!', 'message': 'Participante não se registrou para esse evento'})
        if event.attendee_checkedin(attendee):
            return response.Response({'status': 'error', 'title': 'Opa!', 'message': 'Participante já fez check-in nesse evento'})
        return response.Response({'status': 'success', 'title': attendee.shortcuts.full_name, 'message': f'Fazer check-in em {event.name}?'})


class CheckinAttendee(views.APIView):
    permission_classes = [IsStaff]

    def post(self, request):
        event_id = request.data.get('event_id', None)
        unique_id = request.data.get('unique_id', None)
        event = Event.objects.filter(pk=event_id)
        if not event.exists():
            return response.Response({'status': 'error', 'title': 'Opa!', 'message': 'Evento inválido'})
        attendee = Profile.objects.filter(unique_id=unique_id)
        if not attendee.exists():
            return response.Response({'status': 'error', 'title': 'Opa!', 'message': 'Participante inválido'})
        event = event[0]
        attendee = attendee[0]
        if event.attendee_checkedin(attendee):
            return response.Response({'status': 'error', 'title': 'Opa!', 'message': 'Participante já fez check-in nesse evento'})
        checkedin = event.checkin_attendee(attendee)
        if not checkedin:
            return response.Response({'status': 'error', 'title': 'Opa!', 'message': 'Participante não se registrou para esse evento'})
        return response.Response({'status': 'success', 'title': 'Pronto!', 'message': 'Check-in completo'})
