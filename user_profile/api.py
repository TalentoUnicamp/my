from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework import views
from django.contrib.auth import login
from django.conf import settings
from godmode.permissions import IsAdmin
from staff.permissions import IsStaff
from .models import Profile, User
from .tasks import send_recover_token_email
from .serializers import ListProfileSerializer, ListHackerProfileSerializer
import time


class CheckToken(views.APIView):

    def post(self, request):
        token = request.data.get('token')
        try:
            instance = Profile.objects.get(token=token)
            login(request, instance.user)
            return views.Response({'redirect_url': request.GET.get('next', settings.PROFILE_REDIRECT_URL)})
        except Profile.DoesNotExist:
            time.sleep(2)
            return views.Response({'error': 'Token inválido'}, status=404)


class ResetTokenEmail(views.APIView):

    def post(self, request):
        email = request.data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            user = user.first()
            user.profile.new_token()
            send_recover_token_email.delay(user.profile.id)
        time.sleep(2)
        return views.Response({'message': 'Olhe seu email :)'})


class ChangeEmail(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        email = request.data.get('email')
        user = request.user
        user.profile.change_email(email)
        time.sleep(2)
        return views.Response({'message': 'Olhe seu email :)'})


class ChangeToken(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        token = user.profile.new_token()
        return views.Response({'message': 'Token alterado', 'token': token})


class ListProfiles(ListAPIView):
    serializer_class = ListProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAdmin]


class ListHackerProfiles(ListAPIView):
    serializer_class = ListHackerProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsStaff]

    def get_queryset(self):
        queryset = super().get_queryset()
        hacker_list = [profile for profile in queryset if profile.state in ['checkedin', 'confirmed', 'waitlist', 'admitted', 'submitted', 'declined']]
        return hacker_list
