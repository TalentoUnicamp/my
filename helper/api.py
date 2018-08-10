from rest_framework import views, viewsets, mixins, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_condition import And, Or
from project.generics import PrefetchRetrieveAPIView
from project.permissions import IsPostRequest, IsGetRequest, IsPutPatchRequest, IsDeleteRequest, OwnsObject
from godmode.permissions import IsAdmin
from user_profile.models import Profile
from project.mixins import PrefetchQuerysetModelMixin
from .permissions import IsMentor, CanSubmitTickets
from .models import Mentor, Ticket
from .serializers import TicketSerializer, MentorSerializer


class ToggleIsMentor(views.APIView):
    permission_classes = [IsAdmin]

    def post(self, request):
        unique_id = request.data['unique_id']
        profile = Profile.objects.get(unique_id=unique_id)
        if profile.is_mentor:
            profile.mentor.delete()
            profile.trigger_update()
        else:
            mentor = Mentor(profile=profile)
            mentor.save()
        return views.Response({'message': 'Permissão alterada'})


class TicketViewset(
        PrefetchQuerysetModelMixin,
        viewsets.ModelViewSet):
    ownership_field = "creator"
    user_relation = "user.profile"
    permission_classes = [
        Or(
            And(IsPostRequest, CanSubmitTickets),   # Creating new tickets
            And(IsDeleteRequest, Or(
                IsAdmin,  # Admin deleting ticket
                And(CanSubmitTickets, OwnsObject),  # Deleting own ticket
            )),
            And(IsGetRequest, CanSubmitTickets),  # Geting last ticket, or list of tickets
            And(IsPutPatchRequest, Or(
                IsMentor,   # Mentors manipulating tickets
                And(CanSubmitTickets, OwnsObject)   # Submitting feedback
            ))
        )
    ]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(methods=['get'], detail=False)
    def last_ticket(self, request):
        self.update
        ticket = Ticket.objects.filter(creator=request.user.profile).last()
        if ticket is not None:
            self.queryset = Ticket.objects.filter(id=ticket.id)
            queryset = self.get_queryset()
        else:
            queryset = Ticket.objects.none()
        serializer = self.get_serializer_class()(queryset, many=True)
        data = serializer.data[0] if len(serializer.data) > 0 else {}
        return Response(data)


class MentorViewset(
        PrefetchQuerysetModelMixin,
        viewsets.ModelViewSet):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [
        Or(
            IsAdmin,
            And(IsGetRequest, CanSubmitTickets)
        )
    ]


class OnlineMentorViewset(
        PrefetchRetrieveAPIView,
        mixins.ListModelMixin,
        viewsets.GenericViewSet):
    permission_classes = [Or(IsAdmin, CanSubmitTickets)]
    queryset = Mentor.objects.filter(online=True)
    serializer_class = MentorSerializer


class SelfMentor(
        PrefetchQuerysetModelMixin,
        generics.RetrieveUpdateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    permission_classes = [IsMentor]

    def get_object(self):
        return self.get_queryset().get(profile=self.request.user.profile)
