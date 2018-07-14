from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from settings.permissions import CanConfirm
from .permissions import IsAdmitted, IsWithdraw, IsHacker
from rest_framework import views, generics
from .models import Hacker
from .serializers import ListHackersSerializers

from staff.permissions import IsStaff


class ConfirmPresence(views.APIView):

    permission_classes = [IsAuthenticated, IsAdmitted, CanConfirm]

    def post(self, request):
        hacker = request.user.profile.hacker
        hacker.confirm()
        return views.Response({'message': 'Presença confirmada', 'state': hacker.profile.state})


class Withdraw(views.APIView):

    permission_classes = [IsAuthenticated, IsHacker]

    def post(self, request):
        hacker = request.user.profile.hacker
        hacker.withdraw_from_event()
        return views.Response({'message': 'Desistência completa', 'state': hacker.profile.state})


class UndoWithdraw(views.APIView):

    permission_classes = [IsAuthenticated, IsWithdraw, CanConfirm]

    def post(self, request):
        hacker = request.user.profile.hacker
        hacker.admit(False)
        return views.Response({'message': 'Desistência desfeita', 'state': hacker.profile.state})


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10


class ListHackersView(generics.ListAPIView):
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated, IsStaff]
    queryset = Hacker.objects.exclude(withdraw=True).exclude(declined=True).exclude(waitlist=True)
    serializer_class = ListHackersSerializers
